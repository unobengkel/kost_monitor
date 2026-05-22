"""
Main Entry Point: Aplikasi Server Monitoring Listrik Kost

Flask server yang menyediakan REST API untuk perangkat ESP8266
dan frontend web monitoring.
"""

import os
import sys
from flask import Flask, send_from_directory, jsonify

# Tambahkan parent directory ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.repositories import JsonDeviceRepository, JsonSensorRepository
from app.application.services import DeviceService, MonitoringService
from app.presentation.routes import api_bp, init_routes


def create_app(static_folder: str = None) -> Flask:
    """
    Factory function untuk membuat Flask application.
    
    Args:
        static_folder: Path ke folder static (web). Jika None, tidak serve static files.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, static_folder=static_folder, static_url_path="")
    
    # ================================================================
    # INISIALISASI DEPENDENCIES
    # ================================================================
    device_repo = JsonDeviceRepository()
    sensor_repo = JsonSensorRepository()
    
    device_service = DeviceService(device_repo, sensor_repo)
    monitoring_service = MonitoringService(device_repo, sensor_repo)
    
    # ================================================================
    # DAFTARKAN ROUTES API
    # ================================================================
    init_routes(device_service, monitoring_service)
    app.register_blueprint(api_bp)
    
    # ================================================================
    # SEED DATA: Daftarkan perangkat default jika belum ada
    # ================================================================
    with app.app_context():
        _seed_default_devices(device_service)
    
    # ================================================================
    # ROUTE: Serve frontend web (SPA)
    # ================================================================
    if static_folder and os.path.isdir(static_folder):
        @app.route("/")
        def index():
            return send_from_directory(static_folder, "index.html")
        
        @app.route("/<path:path>")
        def static_files(path):
            file_path = os.path.join(static_folder, path)
            if os.path.isfile(file_path):
                return send_from_directory(static_folder, path)
            else:
                # Fallback ke index.html untuk SPA routing
                return send_from_directory(static_folder, "index.html")
    
    return app


def _seed_default_devices(device_service: DeviceService):
    """Menambahkan data perangkat default jika belum ada."""
    default_devices = [
        ("kamar_01", "Kamar A", 900.0),
        ("kamar_02", "Kamar B", 900.0),
        ("kamar_03", "Kamar C", 900.0),
    ]
    
    for device_id, nama_kamar, batas_daya in default_devices:
        try:
            device_service.register_device(device_id, nama_kamar, batas_daya)
            print(f"  [SEED] Device '{device_id}' ({nama_kamar}) berhasil didaftarkan")
        except ValueError:
            pass  # Device sudah ada, abaikan


# ================================================================
# MAIN: Jalankan server
# ================================================================
if __name__ == "__main__":
    # Path ke folder web (frontend SPA)
    web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
    
    # Jika folder web tidak ada, jalan tanpa frontend
    if not os.path.isdir(web_dir):
        web_dir = None
    
    app = create_app(static_folder=web_dir)
    
    print("=" * 55)
    print("  SISTEM MONITORING LISTRIK KOST - SERVER v1.0")
    print("=" * 55)
    print()
    print("  REST API Endpoints:")
    print("    GET  /api/health              - Health check")
    print("    GET  /api/dashboard           - Data dashboard")
    print("    GET  /api/devices             - Daftar semua perangkat")
    print("    GET  /api/device/<id>         - Detail perangkat")
    print("    POST /api/device/data         - Terima data sensor (ESP8266)")
    print("    GET  /api/device/command/<id> - Ambil perintah relay (ESP8266)")
    print("    POST /api/device/<id>/relay   - Kontrol relay")
    print("    POST /api/device/register     - Daftar perangkat baru")
    print("    PUT  /api/device/<id>/batas-daya - Update batas daya")
    print("    GET  /api/device/<id>/history - Riwayat data sensor")
    print()
    
    if web_dir:
        print(f"  Frontend Web: http://localhost:5000")
    else:
        print("  Frontend Web: Tidak tersedia (folder 'web/' tidak ditemukan)")
    
    print()
    print(f"  Server berjalan di: http://localhost:5000")
    print("=" * 55)
    
    # Jalankan server Flask
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )