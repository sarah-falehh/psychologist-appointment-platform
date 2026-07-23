import re
import sqlite3

from datetime import date, datetime
from functools import wraps
from pathlib import Path
from flask import (
    Flask,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from content import CONTENT


# =========================================================
# CONFIGURATION DE L'APPLICATION
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-secret-key-before-production"

SUPPORTED_LANGUAGES = ["fr", "ar", "en"]

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FOLDER = BASE_DIR / "database"
DATABASE_PATH = DATABASE_FOLDER / "psychologue.db"


# Identifiants temporaires de développement uniquement
ADMIN_EMAIL = "admin@psychologue.tn"
ADMIN_PASSWORD = "Admin123!"

# Cette valeur permet aussi d'invalider les anciennes sessions admin.
ADMIN_SESSION_VERSION = "admin-session-v2"


AVAILABLE_SLOTS = [
    "09:00",
    "10:00",
    "11:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
]


ALLOWED_CONSULTATION_TYPES = {
    "premiere-consultation",
    "suivi",
    "guidance-parentale",
    "bilan",
}


NAME_PATTERN = re.compile(
    r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$",
    re.UNICODE,
)

EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

PHONE_PATTERN = re.compile(
    r"^(?:\+216)?[24579]\d{7}$"
)


# =========================================================
# LANGUES ET TRADUCTIONS
# =========================================================

def get_current_language():
    language = session.get("language", "fr")

    if language not in SUPPORTED_LANGUAGES:
        return "fr"

    return language


@app.context_processor
def inject_translations():
    language = get_current_language()

    return {
        "language": language,
        "content": CONTENT[language],
        "direction": CONTENT[language]["direction"],
        "current_app": current_app,
    }


@app.context_processor
def inject_notifications():
    notifications = []
    unread = 0

    if session.get("admin_logged_in"):
        notifications, unread = get_notifications("admin")
    elif session.get("user_id"):
        notifications, unread = get_notifications(
            f"patient_{session['user_id']}"
        )

    return {
        "notifications": notifications,
        "unread_notifications": unread,
    }
@app.route("/langue/<language_code>")
def change_language(language_code):
    if language_code in SUPPORTED_LANGUAGES:
        session["language"] = language_code

    previous_page = request.referrer

    if previous_page:
        return redirect(previous_page)

    return redirect(url_for("index"))


# =========================================================
# BASE DE DONNÉES
# =========================================================

def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    # Active réellement les clés étrangères dans SQLite.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
# =====================================
# NOTIFICATIONS
# =====================================

def create_notification(receiver, title, body="", link=""):
    connection = get_database_connection()

    connection.execute(
        """
        INSERT INTO notifications (
            receiver,
            title,
            body,
            link
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            receiver,
            title,
            body,
            link,
        ),
    )

    connection.commit()
    connection.close()


def get_notifications(receiver):
    connection = get_database_connection()

    notifications = connection.execute(
        """
        SELECT *
        FROM notifications
        WHERE receiver = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 10
        """,
        (receiver,),
    ).fetchall()

    unread = connection.execute(
        """
        SELECT COUNT(*) AS total
        FROM notifications
        WHERE receiver = ?
          AND is_read = 0
        """,
        (receiver,),
    ).fetchone()["total"]

    connection.close()

    return notifications, unread


def send_message(sender_id, receiver_id, message):

    connection = get_database_connection()

    connection.execute(
        """
        INSERT INTO messages(

            sender_id,
            receiver_id,
            message

        )

        VALUES (?, ?, ?)

        """,

        (
            sender_id,
            receiver_id,
            message
        )
    )

    connection.commit()

    connection.close()
def ensure_notifications_table(connection):
    """Crée ou migre la table notifications vers le schéma receiver."""

    table_exists = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'notifications'
        """
    ).fetchone()

    if table_exists is None:
        connection.execute(
            """
            CREATE TABLE notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receiver TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT,
                link TEXT,
                is_read INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        return

    columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(notifications)"
        ).fetchall()
    }

    if "receiver" in columns:
        return

    connection.execute(
        "ALTER TABLE notifications RENAME TO notifications_legacy"
    )

    connection.execute(
        """
        CREATE TABLE notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receiver TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT,
            link TEXT,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    legacy_columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(notifications_legacy)"
        ).fetchall()
    }

    if "user_id" in legacy_columns:
        connection.execute(
            """
            INSERT INTO notifications (
                receiver,
                title,
                body,
                link,
                is_read,
                created_at
            )
            SELECT
                'patient_' || user_id,
                title,
                body,
                link,
                COALESCE(is_read, 0),
                created_at
            FROM notifications_legacy
            """
        )

    connection.execute("DROP TABLE notifications_legacy")


def create_database():
    DATABASE_FOLDER.mkdir(exist_ok=True)

    connection = get_database_connection()

    # Il faut créer users avant appointments,
    # car appointments contient une clé étrangère vers users.
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            consultation_type TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            preferred_time TEXT NOT NULL,
            message TEXT,
            consent INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'En attente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
        
    )
    # ==========================
# TABLE MESSAGES
# ==========================

    connection.execute("""
CREATE TABLE IF NOT EXISTS messages (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sender_id INTEGER NOT NULL,

    receiver_id INTEGER NOT NULL,

    message TEXT NOT NULL,

    is_read INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(sender_id) REFERENCES users(id),

    FOREIGN KEY(receiver_id) REFERENCES users(id)

)
""")

    # ==========================
    # TABLE NOTIFICATIONS
    # ==========================

    ensure_notifications_table(connection)

    # ==========================
    # TABLE CHAT_MESSAGES
    # ==========================

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            sender_role TEXT NOT NULL
                CHECK (sender_role IN ('patient', 'admin')),
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (patient_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# OUTILS DE SESSION
# =========================================================

def clear_patient_session():
    """
    Supprime uniquement les données de connexion du patient.
    La langue sélectionnée est conservée.
    """

    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("user_email", None)
    session.pop("user_phone", None)


def clear_admin_session():
    """
    Supprime uniquement les données de connexion administrateur.
    """

    session.pop("admin_logged_in", None)
    session.pop("admin_email", None)
    session.pop("admin_session_version", None)


def admin_required(route_function):
    @wraps(route_function)
    def protected_route(*args, **kwargs):
        admin_logged_in = session.get("admin_logged_in")
        admin_email = session.get("admin_email")
        admin_version = session.get("admin_session_version")

        admin_session_is_valid = (
            admin_logged_in is True
            and admin_email == ADMIN_EMAIL
            and admin_version == ADMIN_SESSION_VERSION
        )

        if not admin_session_is_valid:
            clear_admin_session()

            flash(
                "Veuillez vous connecter avec le compte administrateur.",
                "error",
            )

            return redirect(url_for("admin_login"))

        return route_function(*args, **kwargs)

    return protected_route
def patient_required(route_function):
    @wraps(route_function)
    def protected_route(*args, **kwargs):
        if not session.get("user_id"):
            flash(
                "Veuillez vous connecter pour accéder à la messagerie.",
                "error",
            )
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return protected_route

# =========================================================
# OUTILS DE VALIDATION
# =========================================================

def normalize_phone(phone):
    """
    Exemples acceptés :
    20 194 015
    +216 20 194 015
    20194015
    """

    return re.sub(
        r"[\s().-]",
        "",
        phone,
    )


# =========================================================
# PAGES PUBLIQUES
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/a-propos")
def about():
    return render_template("about.html")


@app.route("/accompagnements")
def services():
    return render_template("services.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================================================
# INSCRIPTION PATIENT
# =========================================================

@app.route("/inscription", methods=["GET", "POST"])
def signup():
    if session.get("user_id"):
        return redirect(url_for("patient_dashboard"))

    if request.method == "POST":
        full_name = request.form.get(
            "full_name",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        phone = request.form.get(
            "phone",
            "",
        ).strip()

        password = request.form.get(
            "password",
            "",
        )

        confirm_password = request.form.get(
            "confirm_password",
            "",
        )

        if not full_name:
            flash(
                "Veuillez renseigner votre nom et prénom.",
                "error",
            )
            return render_template("signup.html")

        if len(full_name) < 2 or len(full_name) > 100:
            flash(
                "Le nom doit contenir entre 2 et 100 caractères.",
                "error",
            )
            return render_template("signup.html")

        if not NAME_PATTERN.fullmatch(full_name):
            flash(
                "Le nom ne doit contenir que des lettres, "
                "des espaces, des apostrophes ou des tirets.",
                "error",
            )
            return render_template("signup.html")

        if not email:
            flash(
                "Veuillez renseigner votre adresse e-mail.",
                "error",
            )
            return render_template("signup.html")

        if not EMAIL_PATTERN.fullmatch(email):
            flash(
                "Veuillez saisir une adresse e-mail valide.",
                "error",
            )
            return render_template("signup.html")

        normalized_phone = normalize_phone(phone)

        if phone and not PHONE_PATTERN.fullmatch(normalized_phone):
            flash(
                "Veuillez saisir un numéro tunisien valide.",
                "error",
            )
            return render_template("signup.html")

        if len(password) < 8:
            flash(
                "Le mot de passe doit contenir au moins 8 caractères.",
                "error",
            )
            return render_template("signup.html")

        if password != confirm_password:
            flash(
                "Les deux mots de passe ne correspondent pas.",
                "error",
            )
            return render_template("signup.html")

        connection = get_database_connection()

        existing_user = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if existing_user is not None:
            connection.close()

            flash(
                "Un compte existe déjà avec cette adresse e-mail.",
                "error",
            )
            return render_template("signup.html")

        password_hash = generate_password_hash(password)

        cursor = connection.execute(
            """
            INSERT INTO users (
                full_name,
                email,
                phone,
                password_hash
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                normalized_phone,
                password_hash,
            ),
        )

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        # Un patient qui se connecte ne doit pas conserver
        # une éventuelle ancienne session administrateur.
        clear_admin_session()

        session["user_id"] = user_id
        session["user_name"] = full_name
        session["user_email"] = email
        session["user_phone"] = normalized_phone

        flash(
            "Votre compte a été créé avec succès.",
            "success",
        )

        return redirect(url_for("patient_dashboard"))

    return render_template("signup.html")


# =========================================================
# CONNEXION PATIENT
# =========================================================

@app.route("/connexion", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("patient_dashboard"))

    if request.method == "POST":
        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        if not email or not password:
            flash(
                "Veuillez renseigner votre e-mail et votre mot de passe.",
                "error",
            )
            return render_template("login.html")

        connection = get_database_connection()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        connection.close()

        if user is None:
            flash(
                "Adresse e-mail ou mot de passe incorrect.",
                "error",
            )
            return render_template("login.html")

        if not check_password_hash(
            user["password_hash"],
            password,
        ):
            flash(
                "Adresse e-mail ou mot de passe incorrect.",
                "error",
            )
            return render_template("login.html")

        # On supprime une éventuelle ancienne session admin.
        clear_admin_session()

        session["user_id"] = user["id"]
        session["user_name"] = user["full_name"]
        session["user_email"] = user["email"]
        session["user_phone"] = user["phone"] or ""

        flash(
            "Vous êtes maintenant connecté.",
            "success",
        )

        return redirect(url_for("patient_dashboard"))

    return render_template("login.html")


@app.route("/deconnexion")
def logout():
    clear_patient_session()

    flash(
        "Vous avez été déconnecté de votre espace patient.",
        "success",
    )

    return redirect(url_for("index"))


# =========================================================
# CRÉNEAUX DISPONIBLES
# =========================================================

@app.route("/api/creneaux")
def available_slots():
    appointment_date = request.args.get(
        "date",
        "",
    ).strip()

    if not appointment_date:
        return jsonify(
            {
                "success": False,
                "slots": [],
            }
        ), 400

    try:
        selected_date = datetime.strptime(
            appointment_date,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return jsonify(
            {
                "success": False,
                "slots": [],
            }
        ), 400

    if selected_date < date.today():
        return jsonify(
            {
                "success": False,
                "slots": [],
            }
        ), 400

    # Fermeture le dimanche.
    if selected_date.weekday() == 6:
        return jsonify(
            {
                "success": True,
                "slots": [],
            }
        )

    connection = get_database_connection()

    booked_rows = connection.execute(
        """
        SELECT preferred_time
        FROM appointments
        WHERE appointment_date = ?
          AND status != 'Annulé'
        """,
        (appointment_date,),
    ).fetchall()

    connection.close()

    booked_slots = {
        row["preferred_time"]
        for row in booked_rows
    }

    free_slots = [
        slot
        for slot in AVAILABLE_SLOTS
        if slot not in booked_slots
    ]

    return jsonify(
        {
            "success": True,
            "slots": free_slots,
        }
    )


# =========================================================
# PRISE DE RENDEZ-VOUS
# =========================================================

@app.route("/rendez-vous", methods=["GET", "POST"])
def appointment():
    if not session.get("user_id"):
        flash(
            "Veuillez créer un compte ou vous connecter "
            "pour prendre un rendez-vous.",
            "error",
        )
        return redirect(url_for("login"))

    if request.method == "POST":
        full_name = request.form.get(
            "full_name",
            "",
        ).strip()

        phone = request.form.get(
            "phone",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        consultation_type = request.form.get(
            "consultation_type",
            "",
        ).strip()

        appointment_date = request.form.get(
            "appointment_date",
            "",
        ).strip()

        preferred_time = request.form.get(
            "preferred_time",
            "",
        ).strip()

        message = request.form.get(
            "message",
            "",
        ).strip()

        consent = request.form.get("consent")

        form_data = {
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "consultation_type": consultation_type,
            "appointment_date": appointment_date,
            "preferred_time": preferred_time,
            "message": message,
        }

        if not full_name:
            flash(
                "Veuillez renseigner votre nom et prénom.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if len(full_name) < 2 or len(full_name) > 100:
            flash(
                "Le nom doit contenir entre 2 et 100 caractères.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if not NAME_PATTERN.fullmatch(full_name):
            flash(
                "Le nom contient des caractères non autorisés.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        normalized_phone = normalize_phone(phone)

        if not normalized_phone:
            flash(
                "Veuillez renseigner votre numéro de téléphone.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if not PHONE_PATTERN.fullmatch(normalized_phone):
            flash(
                "Veuillez saisir un numéro tunisien valide.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if not email or not EMAIL_PATTERN.fullmatch(email):
            flash(
                "Veuillez saisir une adresse e-mail valide.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if consultation_type not in ALLOWED_CONSULTATION_TYPES:
            flash(
                "Veuillez sélectionner un type de consultation valide.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if not appointment_date:
            flash(
                "Veuillez sélectionner une date.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        try:
            selected_date = datetime.strptime(
                appointment_date,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            flash(
                "La date sélectionnée est invalide.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if selected_date < date.today():
            flash(
                "Vous ne pouvez pas sélectionner une date passée.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if selected_date.weekday() == 6:
            flash(
                "Le cabinet est fermé le dimanche.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if preferred_time not in AVAILABLE_SLOTS:
            flash(
                "Veuillez sélectionner un créneau horaire valide.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if len(message) > 500:
            flash(
                "Le motif général ne doit pas dépasser 500 caractères.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        if consent != "on":
            flash(
                "Vous devez accepter l’utilisation de vos coordonnées.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        connection = get_database_connection()

        existing_appointment = connection.execute(
            """
            SELECT id
            FROM appointments
            WHERE appointment_date = ?
              AND preferred_time = ?
              AND status != 'Annulé'
            """,
            (
                appointment_date,
                preferred_time,
            ),
        ).fetchone()

        if existing_appointment is not None:
            connection.close()

            flash(
                "Ce créneau vient d’être réservé. "
                "Veuillez en choisir un autre.",
                "error",
            )
            return render_template(
                "appointment.html",
                form_data=form_data,
            )

        connection.execute(
            """
            INSERT INTO appointments (
                user_id,
                full_name,
                phone,
                email,
                consultation_type,
                appointment_date,
                preferred_time,
                message,
                consent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                full_name,
                normalized_phone,
                email,
                consultation_type,
                appointment_date,
                preferred_time,
                message,
                1,
            ),
        )

        connection.commit()
        connection.close()

        create_notification(
            "admin",
            "Nouveau rendez-vous",
            f"{full_name} vient de demander un rendez-vous.",
            "/admin",
        )

        return redirect(
            url_for("appointment_success")
        )

    return render_template(
        "appointment.html",
        form_data={},
    )


@app.route("/rendez-vous/confirmation")
def appointment_success():
    return render_template(
        "appointment_success.html"
    )


# =========================================================
# ESPACE PATIENT
# =========================================================

@app.route("/mon-espace")
def patient_dashboard():
    if not session.get("user_id"):
        flash(
            "Veuillez vous connecter pour accéder à votre espace.",
            "error",
        )
        return redirect(url_for("login"))

    connection = get_database_connection()

    appointments = connection.execute(
        """
        SELECT *
        FROM appointments
        WHERE user_id = ?
        ORDER BY appointment_date ASC,
                 preferred_time ASC,
                 created_at DESC
        """,
        (session["user_id"],),
    ).fetchall()

    connection.close()

    return render_template(
        "patient_dashboard.html",
        appointments=appointments,
    )


@app.route(
    "/mon-espace/rendez-vous/<int:appointment_id>/annuler",
    methods=["POST"],
)
def cancel_patient_appointment(appointment_id):
    if not session.get("user_id"):
        flash(
            "Veuillez vous connecter.",
            "error",
        )
        return redirect(url_for("login"))

    connection = get_database_connection()

    appointment_record = connection.execute(
        """
        SELECT *
        FROM appointments
        WHERE id = ?
          AND user_id = ?
        """,
        (
            appointment_id,
            session["user_id"],
        ),
    ).fetchone()

    if appointment_record is None:
        connection.close()

        flash(
            "Ce rendez-vous est introuvable.",
            "error",
        )
        return redirect(url_for("patient_dashboard"))

    if appointment_record["status"] != "En attente":
        connection.close()

        flash(
            "Seuls les rendez-vous en attente "
            "peuvent être annulés depuis votre espace.",
            "error",
        )
        return redirect(url_for("patient_dashboard"))

    connection.execute(
        """
        UPDATE appointments
        SET status = 'Annulé'
        WHERE id = ?
          AND user_id = ?
        """,
        (
            appointment_id,
            session["user_id"],
        ),
    )

    connection.commit()
    connection.close()

    flash(
        "Votre demande de rendez-vous a été annulée.",
        "success",
    )

    return redirect(url_for("patient_dashboard"))
# =========================================================
# MESSAGERIE PATIENT
# =========================================================

@app.route("/mon-espace/messages", methods=["GET", "POST"])
@patient_required
def patient_messages():
    patient_id = session["user_id"]

    connection = get_database_connection()

    if request.method == "POST":
        message = request.form.get(
            "message",
            "",
        ).strip()

        if not message:
            connection.close()

            flash(
                "Le message ne peut pas être vide.",
                "error",
            )
            return redirect(url_for("patient_messages"))

        if len(message) > 1500:
            connection.close()

            flash(
                "Le message ne doit pas dépasser 1 500 caractères.",
                "error",
            )
            return redirect(url_for("patient_messages"))

        connection.execute(
            """
            INSERT INTO chat_messages (
                patient_id,
                sender_role,
                message
            )
            VALUES (?, 'patient', ?)
            """,
            (
                patient_id,
                message,
            ),
        )

        connection.commit()
        connection.close()

        create_notification(
            "admin",
            "Nouveau message",
            f"{session.get('user_name')} vous a envoyé un message.",
            f"/admin/messages/{patient_id}",
        )

        return redirect(url_for("patient_messages"))

    connection.execute(
        """
        UPDATE chat_messages
        SET is_read = 1
        WHERE patient_id = ?
          AND sender_role = 'admin'
        """,
        (patient_id,),
    )

    messages = connection.execute(
        """
        SELECT *
        FROM chat_messages
        WHERE patient_id = ?
        ORDER BY created_at ASC, id ASC
        """,
        (patient_id,),
    ).fetchall()

    connection.commit()
    connection.close()

    return render_template(
        "patient_messages.html",
        messages=messages,
    )

# =========================================================
# CONNEXION ADMINISTRATEUR
# =========================================================

@app.route("/admin/connexion", methods=["GET", "POST"])
def admin_login():
    admin_session_is_valid = (
        session.get("admin_logged_in") is True
        and session.get("admin_email") == ADMIN_EMAIL
        and session.get("admin_session_version")
        == ADMIN_SESSION_VERSION
    )

    if admin_session_is_valid:
        return redirect(url_for("admin_dashboard"))

    # Supprime une ancienne session admin incomplète ou périmée.
    clear_admin_session()

    if request.method == "POST":
        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        if (
            email == ADMIN_EMAIL.lower()
            and password == ADMIN_PASSWORD
        ):
            # L'administrateur ne doit pas rester connecté
            # en même temps avec un compte patient.
            clear_patient_session()

            session["admin_logged_in"] = True
            session["admin_email"] = ADMIN_EMAIL
            session["admin_session_version"] = ADMIN_SESSION_VERSION

            flash(
                "Connexion administrateur réussie.",
                "success",
            )

            return redirect(url_for("admin_dashboard"))

        flash(
            "Identifiants administrateur incorrects.",
            "error",
        )

    return render_template("admin_login.html")


# =========================================================
# TABLEAU DE BORD ADMINISTRATEUR
# =========================================================

@app.route("/admin")
@admin_required
def admin_dashboard():
    status_filter = request.args.get(
        "status",
        "all",
    ).strip()

    search_query = request.args.get(
        "search",
        "",
    ).strip()

    sort_order = request.args.get(
        "sort",
        "date_asc",
    ).strip()

    allowed_statuses = {
        "all",
        "En attente",
        "Confirmé",
        "Annulé",
    }

    if status_filter not in allowed_statuses:
        status_filter = "all"

    allowed_sorts = {
        "date_asc",
        "date_desc",
        "created_desc",
    }

    if sort_order not in allowed_sorts:
        sort_order = "date_asc"

    query = """
        SELECT *
        FROM appointments
        WHERE 1 = 1
    """

    parameters = []

    if status_filter != "all":
        query += """
            AND status = ?
        """
        parameters.append(status_filter)

    if search_query:
        query += """
            AND (
                full_name LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
            )
        """

        search_pattern = f"%{search_query}%"

        parameters.extend(
            [
                search_pattern,
                search_pattern,
                search_pattern,
            ]
        )

    if sort_order == "date_desc":
        query += """
            ORDER BY appointment_date DESC,
                     preferred_time DESC
        """

    elif sort_order == "created_desc":
        query += """
            ORDER BY created_at DESC
        """

    else:
        query += """
            ORDER BY appointment_date ASC,
                     preferred_time ASC
        """

    connection = get_database_connection()

    appointments = connection.execute(
        query,
        parameters,
    ).fetchall()

    statistics_row = connection.execute(
        """
        SELECT
            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN status = 'En attente'
                    THEN 1
                    ELSE 0
                END
            ) AS pending,

            SUM(
                CASE
                    WHEN status = 'Confirmé'
                    THEN 1
                    ELSE 0
                END
            ) AS confirmed,

            SUM(
                CASE
                    WHEN status = 'Annulé'
                    THEN 1
                    ELSE 0
                END
            ) AS cancelled

        FROM appointments
        """
    ).fetchone()

    today_appointments = connection.execute(
        """
        SELECT *
        FROM appointments
        WHERE appointment_date = date('now', 'localtime')
          AND status != 'Annulé'
        ORDER BY preferred_time ASC
        """
    ).fetchall()

    connection.close()

    statistics = {
        "total": statistics_row["total"] or 0,
        "pending": statistics_row["pending"] or 0,
        "confirmed": statistics_row["confirmed"] or 0,
        "cancelled": statistics_row["cancelled"] or 0,
    }

    return render_template(
        "admin_dashboard.html",
        appointments=appointments,
        statistics=statistics,
        today_appointments=today_appointments,
        status_filter=status_filter,
        search_query=search_query,
        sort_order=sort_order,
    )


@app.route(
    "/admin/rendez-vous/<int:appointment_id>/statut",
    methods=["POST"],
)
@admin_required
def update_appointment_status(appointment_id):
    new_status = request.form.get(
        "status",
        "",
    ).strip()

    allowed_statuses = {
        "En attente",
        "Confirmé",
        "Annulé",
    }

    if new_status not in allowed_statuses:
        flash(
            "Le statut sélectionné est invalide.",
            "error",
        )
        return redirect(url_for("admin_dashboard"))

    connection = get_database_connection()

    appointment_record = connection.execute(
        """
        SELECT id
        FROM appointments
        WHERE id = ?
        """,
        (appointment_id,),
    ).fetchone()

    if appointment_record is None:
        connection.close()

        flash(
            "Ce rendez-vous n’existe pas.",
            "error",
        )
        return redirect(url_for("admin_dashboard"))

    connection.execute(
        """
        UPDATE appointments
        SET status = ?
        WHERE id = ?
        """,
        (
            new_status,
            appointment_id,
        ),
    )

    appointment = connection.execute(
        """
        SELECT *
        FROM appointments
        WHERE id = ?
        """,
        (appointment_id,),
    ).fetchone()

    connection.commit()
    connection.close()

    create_notification(
        f"patient_{appointment['user_id']}",
        f"Rendez-vous {new_status}",
        f"Le statut de votre rendez-vous est maintenant : {new_status}.",
        "/mon-espace",
    )

    flash(
        "Le statut du rendez-vous a été mis à jour.",
        "success",
    )

    return redirect(
        request.referrer
        or url_for("admin_dashboard")
    )


@app.route("/admin/deconnexion")
@admin_required
def admin_logout():
    # Ne pas utiliser session.clear(), afin de conserver la langue.
    clear_admin_session()

    flash(
        "Vous avez été déconnecté de l’espace administrateur.",
        "success",
    )

    return redirect(url_for("admin_login"))

# =========================================================
# MESSAGERIE ADMINISTRATEUR
# =========================================================

@app.route("/admin/messages")
@admin_required
def admin_messages():
    connection = get_database_connection()

    conversations = connection.execute(
        """
        SELECT
            users.id AS patient_id,
            users.full_name,
            users.email,
            users.phone,

            (
                SELECT chat_messages.message
                FROM chat_messages
                WHERE chat_messages.patient_id = users.id
                ORDER BY chat_messages.created_at DESC,
                         chat_messages.id DESC
                LIMIT 1
            ) AS last_message,

            (
                SELECT chat_messages.created_at
                FROM chat_messages
                WHERE chat_messages.patient_id = users.id
                ORDER BY chat_messages.created_at DESC,
                         chat_messages.id DESC
                LIMIT 1
            ) AS last_message_at,

            (
                SELECT COUNT(*)
                FROM chat_messages
                WHERE chat_messages.patient_id = users.id
                  AND chat_messages.sender_role = 'patient'
                  AND chat_messages.is_read = 0
            ) AS unread_count

        FROM users

        WHERE EXISTS (
            SELECT 1
            FROM chat_messages
            WHERE chat_messages.patient_id = users.id
        )

        ORDER BY
            last_message_at DESC,
            users.full_name ASC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin_messages.html",
        conversations=conversations,
    )


@app.route(
    "/admin/messages/<int:patient_id>",
    methods=["GET", "POST"],
)
@admin_required
def admin_conversation(patient_id):
    connection = get_database_connection()

    patient = connection.execute(
        """
        SELECT id, full_name, email, phone
        FROM users
        WHERE id = ?
        """,
        (patient_id,),
    ).fetchone()

    if patient is None:
        connection.close()

        flash(
            "Ce patient est introuvable.",
            "error",
        )
        return redirect(url_for("admin_messages"))

    if request.method == "POST":
        message = request.form.get(
            "message",
            "",
        ).strip()

        if not message:
            connection.close()

            flash(
                "Le message ne peut pas être vide.",
                "error",
            )
            return redirect(
                url_for(
                    "admin_conversation",
                    patient_id=patient_id,
                )
            )

        if len(message) > 1500:
            connection.close()

            flash(
                "Le message ne doit pas dépasser 1 500 caractères.",
                "error",
            )
            return redirect(
                url_for(
                    "admin_conversation",
                    patient_id=patient_id,
                )
            )

        connection.execute(
            """
            INSERT INTO chat_messages (
                patient_id,
                sender_role,
                message
            )
            VALUES (?, 'admin', ?)
            """,
            (
                patient_id,
                message,
            ),
        )

        connection.commit()
        connection.close()

        create_notification(
            f"patient_{patient_id}",
            "Nouveau message",
            "La psychologue vous a envoyé un message.",
            "/mon-espace/messages",
        )

        return redirect(
            url_for(
                "admin_conversation",
                patient_id=patient_id,
            )
        )

    connection.execute(
        """
        UPDATE chat_messages
        SET is_read = 1
        WHERE patient_id = ?
          AND sender_role = 'patient'
        """,
        (patient_id,),
    )

    messages = connection.execute(
        """
        SELECT *
        FROM chat_messages
        WHERE patient_id = ?
        ORDER BY created_at ASC, id ASC
        """,
        (patient_id,),
    ).fetchall()

    connection.commit()
    connection.close()

    return render_template(
        "admin_conversation.html",
        patient=patient,
        messages=messages,
    )
# =========================================================
# DÉMARRAGE
# =========================================================

if __name__ == "__main__":
    create_database()

    app.run(debug=True)