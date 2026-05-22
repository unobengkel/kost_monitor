"""
Infrastructure Layer: Repository Implementations

Menggunakan JSON file sebagai penyimpanan data (sederhana, tanpa database).
"""

import json
import os
from typing import Dict, Optional, List
from datetime import datetime
from ..domain.entities import SensorData, Device, RelayCommand


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")


def _ensure_data_dir():
    """Memastikan direktori data ada."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _get_file_path(filename: str) -> str:
    """Mendapatkan path lengkap file data."""
    _ensure_data_dir()
    return os.path.join(DATA_DIR, filename)


def _load_json(filename: str, default: list = None) -> list:
    """Memuat data dari file JSON."""
    filepath = _get_file_path(filename)
    if not os.path.exists(filepath):
        return default or []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default or []


def _save_json(filename: str, data: list):
    """Menyimpan data ke file JSON."""
    filepath = _get_file_path(filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


class JsonDeviceRepository:
    """
    Repository untuk perangkat (device/kamar) menggunakan JSON file.
    """

    def __init__(self):
        self._devices_file = "devices.json"
        self._commands_file = "commands.json"

    def get_all(self) -> List[Device]:
        devices_data = _load_json(self._devices_file)
        devices = []
        for d in devices_data:
            device = Device(
                device_id=d["device_id"],
                nama_kamar=d.get("nama_kamar", ""),
                batas_daya=d.get("batas_daya", 900.0),
                relay_state=d.get("relay_state", "OFF"),
                overload=d.get("overload", False),
                daya_saat_ini=d.get("daya_saat_ini", 0.0),
                arus_saat_ini=d.get("arus_saat_ini", 0.0),
                energi_total=d.get("energi_total", 0.0),
                daya_max=d.get("daya_max", 0.0),
                status_koneksi=d.get("status_koneksi", "OFFLINE"),
                last_seen=datetime.fromisoformat(d["last_seen"]) if d.get("last_seen") else None,
                created_at=datetime.fromisoformat(d["created_at"]) if d.get("created_at") else datetime.now()
            )
            devices.append(device)
        return devices

    def get(self, device_id: str) -> Optional[Device]:
        devices = self.get_all()
        for d in devices:
            if d.device_id == device_id:
                return d
        return None

    def save(self, device: Device):
        devices = self.get_all()
        found = False
        for i, d in enumerate(devices):
            if d.device_id == device.device_id:
                devices[i] = device
                found = True
                break
        if not found:
            devices.append(device)
        
        devices_data = [
            {
                "device_id": d.device_id,
                "nama_kamar": d.nama_kamar,
                "batas_daya": d.batas_daya,
                "relay_state": d.relay_state,
                "overload": d.overload,
                "daya_saat_ini": d.daya_saat_ini,
                "arus_saat_ini": d.arus_saat_ini,
                "energi_total": d.energi_total,
                "daya_max": d.daya_max,
                "status_koneksi": d.status_koneksi,
                "last_seen": d.last_seen.isoformat() if d.last_seen else None,
                "created_at": d.created_at.isoformat()
            }
            for d in devices
        ]
        _save_json(self._devices_file, devices_data)

    def delete(self, device_id: str):
        devices = self.get_all()
        devices = [d for d in devices if d.device_id != device_id]
        devices_data = [
            {
                "device_id": d.device_id,
                "nama_kamar": d.nama_kamar,
                "batas_daya": d.batas_daya,
                "relay_state": d.relay_state,
                "overload": d.overload,
                "daya_saat_ini": d.daya_saat_ini,
                "arus_saat_ini": d.arus_saat_ini,
                "energi_total": d.energi_total,
                "daya_max": d.daya_max,
                "status_koneksi": d.status_koneksi,
                "last_seen": d.last_seen.isoformat() if d.last_seen else None,
                "created_at": d.created_at.isoformat()
            }
            for d in devices
        ]
        _save_json(self._devices_file, devices_data)

    def save_command(self, command: RelayCommand):
        commands = _load_json(self._commands_file)
        commands.append({
            "device_id": command.device_id,
            "command": command.command,
            "issued_at": command.issued_at.isoformat(),
            "executed": command.executed
        })
        _save_json(self._commands_file, commands)

    def get_pending_command(self, device_id: str) -> Optional[Dict]:
        commands = _load_json(self._commands_file)
        for cmd in commands:
            if cmd["device_id"] == device_id and not cmd["executed"]:
                # Tandai sebagai sudah diambil
                cmd["executed"] = True
                _save_json(self._commands_file, commands)
                return {
                    "command": cmd["command"],
                    "issued_at": cmd["issued_at"]
                }
        return None


class JsonSensorRepository:
    """
    Repository untuk data sensor menggunakan JSON file.
    Menyimpan riwayat data sensor per perangkat.
    """

    def __init__(self):
        self._history_file_template = "history_{device_id}.json"
        self._max_records = 500  # Batasi maksimal record per device

    def save(self, data: SensorData):
        filename = self._history_file_template.format(device_id=data.device_id)
        records = _load_json(filename)
        
        records.append({
            "device_id": data.device_id,
            "arus": data.arus,
            "daya": data.daya,
            "tegangan": data.tegangan,
            "relay_state": data.relay_state,
            "overload": data.overload,
            "timestamp": data.timestamp.isoformat()
        })
        
        # Batasi jumlah record
        if len(records) > self._max_records:
            records = records[-self._max_records:]
        
        _save_json(filename, records)

    def get_history(self, device_id: str, limit: int = 50) -> List[SensorData]:
        filename = self._history_file_template.format(device_id=device_id)
        records = _load_json(filename)
        
        # Ambil data terakhir (limit)
        records = records[-limit:]
        
        result = []
        for r in records:
            try:
                data = SensorData(
                    device_id=r["device_id"],
                    arus=float(r.get("arus", 0)),
                    daya=float(r.get("daya", 0)),
                    tegangan=float(r.get("tegangan", 220)),
                    relay_state=r.get("relay_state", "OFF"),
                    overload=bool(r.get("overload", False)),
                    timestamp=datetime.fromisoformat(r["timestamp"])
                )
                result.append(data)
            except (KeyError, ValueError):
                continue
        
        return result