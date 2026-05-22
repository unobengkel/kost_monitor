"""
Presentation Layer: API Routes

Mendefinisikan endpoint REST API untuk komunikasi dengan perangkat ESP8266
dan frontend web.
"""

from flask import Blueprint, request, jsonify
from ..domain.entities import SensorData
from ..application.services import DeviceService, MonitoringService

# Dependency akan di-inject dari app.py
device_service: DeviceService = None
monitoring_service: MonitoringService = None

api_bp = Blueprint("api", __name__, url_prefix="/api")


def init_routes(ds: DeviceService, ms: MonitoringService):
    """Inisialisasi dependency services ke routes."""
    global device_service, monitoring_service
    device_service = ds
    monitoring_service = ms


# ============================================================
# ENDPOINT: Data dari perangkat ESP8266
# ============================================================
@api_bp.route("/device/data", methods=["POST"])
def receive_device_data():
    """
    Menerima data sensor dari perangkat ESP8266.
    
    Request Body (JSON):
    {
        "device_id": "kamar_01",
        "arus": 1.5,
        "daya": 330.0,
        "tegangan": 220.0,
        "relay_state": "ON",
        "overload": false
    }
    
    Response (JSON):
    {
        "status": "ok",
        "command": "RELAY_OFF" (optional, jika overload)
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Data JSON tidak valid"}), 400
        
        # Validasi data wajib
        if "device_id" not in data:
            return jsonify({"status": "error", "message": "device_id wajib diisi"}), 400
        
        # Buat entity SensorData
        sensor_data = SensorData(
            device_id=data["device_id"],
            arus=float(data.get("arus", 0)),
            daya=float(data.get("daya", 0)),
            tegangan=float(data.get("tegangan", 220)),
            relay_state=data.get("relay_state", "OFF"),
            overload=bool(data.get("overload", False))
        )
        
        # Proses data
        result = device_service.process_sensor_data(sensor_data)
        
        response = {"status": "ok"}
        if result and "command" in result:
            response["command"] = result["command"]
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Ambil perintah relay (ESP8266 polling)
# ============================================================
@api_bp.route("/device/command/<device_id>", methods=["GET"])
def get_device_command(device_id):
    """
    Mengambil perintah relay yang tertunda untuk perangkat.
    Dipanggil oleh ESP8266 secara periodik.
    
    Response:
    {
        "command": "RELAY_ON" | "RELAY_OFF" | null
    }
    """
    try:
        command = device_service.get_pending_command(device_id)
        if command:
            return jsonify(command), 200
        else:
            return jsonify({"command": None}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Kontrol relay via web
# ============================================================
@api_bp.route("/device/<device_id>/relay", methods=["POST"])
def control_relay(device_id):
    """
    Mengontrol relay perangkat ON/OFF dari web.
    
    Request Body:
    {
        "command": "RELAY_ON" | "RELAY_OFF"
    }
    """
    try:
        data = request.get_json()
        if not data or "command" not in data:
            return jsonify({"status": "error", "message": "command wajib diisi (RELAY_ON / RELAY_OFF)"}), 400
        
        command = data["command"]
        if command not in ["RELAY_ON", "RELAY_OFF"]:
            return jsonify({"status": "error", "message": "Perintah harus RELAY_ON atau RELAY_OFF"}), 400
        
        result = device_service.control_relay(device_id, command)
        if result is None:
            return jsonify({"status": "error", "message": f"Device '{device_id}' tidak ditemukan"}), 404
        
        return jsonify({"status": "ok", "command": result}), 200
        
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Daftar perangkat baru
# ============================================================
@api_bp.route("/device/register", methods=["POST"])
def register_device():
    """
    Mendaftarkan perangkat baru ke sistem.
    
    Request Body:
    {
        "device_id": "kamar_02",
        "nama_kamar": "Kamar Budi",
        "batas_daya": 900
    }
    """
    try:
        data = request.get_json()
        if not data or "device_id" not in data:
            return jsonify({"status": "error", "message": "device_id wajib diisi"}), 400
        
        device = device_service.register_device(
            device_id=data["device_id"],
            nama_kamar=data.get("nama_kamar", f"Kamar {data['device_id']}"),
            batas_daya=float(data.get("batas_daya", 900))
        )
        
        return jsonify({"status": "ok", "device": device.to_dict()}), 201
        
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Update batas daya
# ============================================================
@api_bp.route("/device/<device_id>/batas-daya", methods=["PUT"])
def update_batas_daya(device_id):
    """
    Mengupdate batas daya perangkat.
    
    Request Body:
    {
        "batas_daya": 1000
    }
    """
    try:
        data = request.get_json()
        if not data or "batas_daya" not in data:
            return jsonify({"status": "error", "message": "batas_daya wajib diisi"}), 400
        
        device = device_service.update_batas_daya(
            device_id=device_id,
            batas_baru=float(data["batas_daya"])
        )
        
        if not device:
            return jsonify({"status": "error", "message": f"Device '{device_id}' tidak ditemukan"}), 404
        
        return jsonify({"status": "ok", "device": device.to_public_dict()}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Dapatkan data semua perangkat
# ============================================================
@api_bp.route("/devices", methods=["GET"])
def get_all_devices():
    """Mendapatkan daftar semua perangkat."""
    try:
        devices = device_service.get_all_devices()
        return jsonify({
            "devices": [d.to_public_dict() for d in devices]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Dapatkan detail perangkat
# ============================================================
@api_bp.route("/device/<device_id>", methods=["GET"])
def get_device_detail(device_id):
    """Mendapatkan detail perangkat."""
    try:
        device = device_service.get_device(device_id)
        if not device:
            return jsonify({"status": "error", "message": f"Device '{device_id}' tidak ditemukan"}), 404
        
        return jsonify({"device": device.to_public_dict()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Dashboard data
# ============================================================
@api_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    """Mendapatkan data dashboard agregat."""
    try:
        data = monitoring_service.get_dashboard_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Riwayat data sensor
# ============================================================
@api_bp.route("/device/<device_id>/history", methods=["GET"])
def get_device_history(device_id):
    """Mendapatkan riwayat data sensor perangkat."""
    try:
        limit = request.args.get("limit", 50, type=int)
        history = monitoring_service.get_device_history(device_id, limit)
        return jsonify({
            "device_id": device_id,
            "history": history
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# ENDPOINT: Health check
# ============================================================
@api_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint health check untuk monitoring server."""
    return jsonify({
        "status": "ok",
        "service": "Sistem Monitoring Listrik Kost",
        "version": "1.0.0"
    }), 200