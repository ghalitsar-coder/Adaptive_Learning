class Soal:
    def __init__(self, soal_id, teks_soal, materi="SPLTV", tingkat="dasar"):
        self.soal_id = soal_id
        self.teks_soal = teks_soal
        self.materi = materi
        self.tingkat = tingkat

    def to_dict(self):
        return {
            "soal_id": self.soal_id,
            "teks_soal": self.teks_soal,
            "materi": self.materi,
            "tingkat": self.tingkat
        }
