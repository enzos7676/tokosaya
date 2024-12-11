from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class NomorHP(models.Model):
    noHp = models.CharField(max_length=20)

    def __str__(self):
        return self.noHp

class Pembeli(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    pekerjaan = models.CharField(max_length=100)
    tanggalLahir = models.DateField()
    noHp = models.ForeignKey(NomorHP, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama


class Penulis(models.Model):
    nama = models.CharField(max_length=100)
    tanggalLahir = models.DateField()
    alamat = models.TextField()

    def __str__(self):
        return self.nama


class Genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre


class Buku(models.Model):
    judulBuku = models.CharField(max_length=200)
    penerbit = models.CharField(max_length=100)
    tahunPenerbit = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    penulis = models.ForeignKey(Penulis, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.judulBuku


class Toko(models.Model):
    namaToko = models.CharField(max_length=100)
    alamat = models.TextField()

    def __str__(self):
        return self.namaToko


class GudangToko(models.Model):
    stok = models.IntegerField()
    toko = models.ForeignKey(Toko, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.toko.namaToko} - {self.buku.judulBuku}"


class Pembelian(models.Model):
    idPem = models.AutoField(primary_key=True)
    waktuPembelian = models.DateTimeField()
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    toko = models.ForeignKey(Toko, on_delete=models.CASCADE)

    def __str__(self):
        return f'Pembelian {self.idPem} - oleh {self.pembeli.nama} - pada {self.waktuPembelian.strftime("%d-%m-%Y %H:%M:%S")}'


class DetailPembelian(models.Model):
    jumlahPieces = models.IntegerField()
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detail {self.id} - {self.buku.judulBuku}"


@receiver(post_save, sender=DetailPembelian)
def update_stok(sender, instance, **kwargs):
    # Mencari stok barang di gudang toko
    try:
        gudang = GudangToko.objects.get(toko=instance.pembelian.toko, buku=instance.buku)
        
        if gudang.stok >= instance.jumlahPieces:
            # Mengurangi stok sesuai dengan jumlah pembelian
            gudang.astok -= instance.jumlahPieces
            gudang.save()
        else:
            raise ValidationError("Stok tidak mencukupi!")  # Jika stok tidak cukup, lemparkan error
    except GudangToko.DoesNotExist:
        raise ValidationError("Buku ini tidak ditemukan di Gudang toko!")
