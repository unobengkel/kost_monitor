"""
Application Services / Use Cases untuk Sistem Monitoring Listrik Kost

Layer ini berisi logika bisnis aplikasi (use cases).
"""

from typing import Dict, Optional, List
from datetime import datetime
from ..domain.entities import SensorData, Device, RelayCommand


class DeviceService:
    """
    Service untuk mengelola perangkat (device/kamar).
    Menyediakan use cases terkait manajemen perangkat.
    """

    def __init__(self, device_repository, sensor_repository):
        self._device_repo = device_repository
        self._sensor_repo = sensor_repository

    def get_all_devices(self) -> List[Device]:
        """Mendapatkan semua perangkat yang terdaftar."""
        return self._device_repo.get_all()

    def get_device(self, device_id: str) -> Optional[Device]:
        """Mendapatkan perangkat berdasarkan device_id."""
        return self._device_repo.get(device_id)

    def register_device(self, device_id: str, nama_kamar: str, batas_daya: float = 900.0) -> Device:
        """Mendaftarkan perangkat baru ke sistem."""
        existing = self._device_repo.get(device_id)
        if existing:
            raise ValueError(f"Device '{device_id}' sudah terdaftar!")
        
        device = Device(
            device_id=device_id,
            nama_kamar=nama_kamar,
            batas_daya=batas_daya
        )
        self._device_repo.save(device)
        return device

    def process_sensor_data(self, data: SensorData) -> Dict:
        """
        Memproses data sensor yang masuk dari perangkat.
        Mengupdate status perangkat dan mengembalikan perintah (jika ada).
        """
        device = self._device_repo.get(data.device_id)
        if not device:
            # Jika perangkat belum terdaftar, daftarkan otomatis
            device = Device(
                device_id=data.device_id,
                nama_kamar=f"Kamar {data.device_id}"
            )
            self._device_repo.save(device)
        
        # Update data perangkat
        device.arus_saat_ini = data.arus
        device.daya_saat_ini = data.daya
        device.relay_state = data.relay_state
        device.overload = data.overload
        device.last_seen = datetime.now()
        device.status_koneksi = "ONLINE"
        
        # Update daya maksimum
        if data.daya > device.daya_max:
            device.daya_max = data.daya
        
        # Update total energi (akumulasi dari perangkat)
        # Energi dihitung di sisi server berdasarkan interval data
        if device.daya_saat_ini > 0:
            # Asumsikan data masuk setiap 5 detik
            device.energi_total += (device.daya_saat_ini / 1000.0) / 720.0
        
        # Simpan riwayat sensor
        self._sensor_repo.save(data)
        
        # Simpan update perangkat
        self._device_repo.save(device)
        
        # Periksa overload
        response = {}
        if data.daya > device.batas_daya and data.relay_state == "ON":
            response["command"] = "RELAY_OFF"
            device.relay_state = "OFF"
            device.overload = True
            self._device_repo.save(device)
        elif data.overload and data.relay_state == "OFF":
            # Device sudah overload, biarkan mati
            pass
        
        return response

    def control_relay(self, device_id: str, command: str) -> Optional[Dict]:
        """
        Mengontrol relay perangkat ON/OFF.
        Menyimpan perintah untuk diambil oleh perangkat nanti.
        """
        device = self._device_repo.get(device_id)
        if not device:
            return None
        
        if command not in ["RELAY_ON", "RELAY_OFF"]:
            raise ValueError("Perintah harus RELAY_ON atau RELAY_OFF")
        
        # Cek overload: jika masih overload, jangan hidupkan
        if command == "RELAY_ON" and device.overload:
            if device.daya_saat_ini > device.batas_daya:
                raise ValueError(
                    f"Tidak bisa menghidupkan relay! Daya saat ini "
                    f"({device.daya_saat_ini:.1f}W) melebihi batas "
                    f"({device.batas_daya:.1f}W)."
                )
            else:
                # Reset overload jika daya sudah turun
                device.overload = False
        
        # Buat perintah relay
        relay_cmd = RelayCommand(
            device_id=device_id,
            command=command
        )
        self._device_repo.save_command(relay_cmd)
        
        # Update status relay
        if command == "RELAY_ON":
            device.relay_state = "ON"
        else:
            device.relay_state = "OFF"
        
        self._device_repo.save(device)
        
        return relay_cmd.to_dict()

    def get_pending_command(self, device_id: str) -> Optional[Dict]:
        """Mengambil perintah relay yang tertunda untuk perangkat."""
        return self._device_repo.get_pending_command(device_id)

    def update_batas_daya(self, device_id: str, batas_baru: float) -> Optional[Device]:
        """Mengupdate batas daya perangkat."""
        device = self._device_repo.get(device_id)
        if not device:
            return None
        
        device.batas_daya = batas_baru
        self._device_repo.save(device)
        return device


class MonitoringService:
    """
    Service untuk monitoring dan dashboard.
    Menyediakan data agregat untuk tampilan web.
    """

    def __init__(self, device_repository, sensor_repository):
        self._device_repo = device_repository
        self._sensor_repo = sensor_repository

    def get_dashboard_data(self) -> Dict:
        """Mendapatkan data untuk dashboard utama."""
        devices = self._device_repo.get_all()
        
        total_daya = sum(d.daya_saat_ini for d in devices)
        total_energi = sum(d.energi_total for d in devices)
        online_count = sum(1 for d in devices if d.status_koneksi == "ONLINE")
        overload_count = sum(1 for d in devices if d.overload)
        
        return {
            "total_devices": len(devices),
            "online_devices": online_count,
            "offline_devices": len(devices) - online_count,
            "overload_count": overload_count,
            "total_daya": round(total_daya, 1),
            "total_energi": round(total_energi, 2),
            "devices": [d.to_public_dict() for d in devices]
        }

    def get_device_history(self, device_id: str, limit: int = 50) -> List[Dict]:
        """Mendapatkan riwayat data sensor perangkat."""
        records = self._sensor_repo.get_history(device_id, limit)
        return [r.to_dict() for r in records]