from django.shortcuts import render
from django.db.models import Sum, Count, F
from tokoadmin.models import DetailPembelian, Pembeli

def homepage(request):
    return render(request, 'homepage.html')

def laporan(request):
    # Top buku terlaris
    top_buku_terlaris = (
        DetailPembelian.objects
        .values('buku__judulBuku')
        .annotate(total_terjual=Sum('jumlahPieces'))
        .order_by('-total_terjual')[:10]
    )
    
    # Top buku dengan pendapatan terbanyak
    top_buku_pendapatan = (
        DetailPembelian.objects
        .values('buku__judulBuku')
        .annotate(total_pendapatan=Sum(F('jumlahPieces') * F('buku__harga')))
        .order_by('-total_pendapatan')[:10]
    )
    
    # Top pekerjaan dengan transaksi terbanyak
    top_pekerjaan_transaksi = (
        Pembeli.objects
        .values('pekerjaan')
        .annotate(jumlah_transaksi=Count('pembelian'))
        .order_by('-jumlah_transaksi')[:10]
    )
    
    context = {
        'top_buku_terlaris': top_buku_terlaris,
        'top_buku_pendapatan': top_buku_pendapatan,
        'top_pekerjaan_transaksi': top_pekerjaan_transaksi,
    }
    return render(request, 'laporan.html', context)



