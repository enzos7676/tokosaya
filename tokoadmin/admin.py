from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import NomorHP, Pembeli, DetailPembelian, GudangToko
from .models import *

class SimpleAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Menampilkan semua field dari model
        return [field.name for field in self.model._meta.fields]


class DetailPembelianAdmin(admin.ModelAdmin):
    list_display = ('id', 'jumlahPieces', 'get_pembelian', 'get_buku')

    def get_pembelian(self, obj):
        return f"{obj.pembelian.pembeli.nama} - {obj.pembelian.waktuPembelian}"
    get_pembelian.short_description = 'Pembelian'

    def get_buku(self, obj):
        return f"{obj.buku.judulBuku} - {obj.buku.penulis.nama}"
    get_buku.short_description = 'Buku'

    def clean(self):
        cleaned_data = super().clean()
        jumlah_pieces = cleaned_data.get('jumlahPieces')
        buku = cleaned_data.get('buku')
        toko = cleaned_data.get('pembelian').toko

        # Cek stok di GudangToko
        try:
            gudang = GudangToko.objects.get(toko=toko, buku=buku)
            if gudang.stok < jumlah_pieces:
                raise ValidationError("Stok tidak mencukupi!")
        except GudangToko.DoesNotExist:
            raise ValidationError("Gudang toko tidak ditemukan!")

        return cleaned_data

# Register model dengan admin
admin.site.register(NomorHP, SimpleAdmin)
admin.site.register(Pembeli, SimpleAdmin)
admin.site.register(Penulis, SimpleAdmin)
admin.site.register(Genre, SimpleAdmin)
admin.site.register(Buku, SimpleAdmin)
admin.site.register(Toko, SimpleAdmin)
admin.site.register(GudangToko, SimpleAdmin)
admin.site.register(Pembelian, SimpleAdmin)
admin.site.register(DetailPembelian, DetailPembelianAdmin)
