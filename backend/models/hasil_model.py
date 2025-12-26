class Siswa:
    def __init__(self, siswa_id, nama, level="pemula"):
        self.siswa_id = siswa_id
        self.nama = nama
        self.level = level

    def to_dict(self):
        return {
            "siswa_id": self.siswa_id,
            "nama": self.nama,
            "level": self.level
        }
