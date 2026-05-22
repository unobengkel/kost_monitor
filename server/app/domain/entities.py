"""
Domain Entities untuk Sistem Monitoring Listrik Kost

Mendefinisikan entitas inti bisnis yang digunakan di seluruh aplikasi.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import json


@dataclass
class SensorData:
    """Data sensor yang dikirim oleh perangkat ESP8266."""
    device_id: str
    arus: float          # Ampere
    daya: float          # Watt
    tegangan: float      # Volt
    relay_state: str     # "ON" / "OFF"
    overload: bool
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "arus": round(self.arus, 3),
            "daya": round(self.daya, 1),
            "tegangan": round(self.tegangan, 1),
            "relay_state": self.relay_state,
            "overload": self.overload,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_json(cls, json_str: str) -> "SensorData":
        data = json.loads(json_str)
        return cls(
            device_id=data["device_id"],
            arus=float(data.get("arus", 0)),
            daya=float(data.get("daya", 0)),
            tegangan=float(data.get("tegangan", 220)),
            relay_state=data.get("relay_state", "OFF"),
            overload=bool(data.get("overload", False))
        )


@dataclass
class Device:
    """Entitas perangkat (kamar) yang terdaftar di sistem."""
    device_id: str
    nama_kamar: str
    batas_daya: float = 900.0        # Watt
    relay_state: str = "OFF"         # "ON" / "OFF"
    overload: bool = False
    daya_saat_ini: float = 0.0       # Watt
    arus_saat_ini: float = 0.0       # Ampere
    energi_total: float = 0.0        # kWh
    daya_max: float = 0.0            # Watt
    status_koneksi: str = "OFFLINE"  # "ONLINE" / "OFFLINE"
    last_seen: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "nama_kamar": self.nama_kamar,
            "batas_daya": self.batas_daya,
            "relay_state": self.relay_state,
            "overload": self.overload,
            "daya_saat_ini": round(self.daya_saat_ini, 1),
            "arus_saat_ini": round(self.arus_saat_ini, 3),
            "energi_total": round(self.energi_total, 4),
            "daya_max": round(self.daya_max, 1),
            "status_koneksi": self.status_koneksi,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "created_at": self.created_at.isoformat()
        }

    def to_public_dict(self) -> dict:
        """Untuk dikirim ke frontend/public tanpa data sensitif."""
        return {
            "device_id": self.device_id,
            "nama_kamar": self.nama_kamar,
            "batas_daya": self.batas_daya,
            "relay_state": self.relay_state,
            "overload": self.overload,
            "daya_saat_ini": round(self.daya_saat_ini, 1),
            "arus_saat_ini": round(self.arus_saat_ini, 3),
            "energi_total": round(self.energi_total, 4),
            "daya_max": round(self.daya_max, 1),
            "status_koneksi": self.status_koneksi,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }


@dataclass
class RelayCommand:
    """Perintah yang dikirim server ke perangkat untuk kontrol relay."""
    device_id: str
    command: str  # "RELAY_ON" / "RELAY_OFF"
    issued_at: datetime = field(default_factory=datetime.now)
    executed: bool = False

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "command": self.command,
            "issued_at": self.issued_at.isoformat(),
            "executed": self.executed
        }