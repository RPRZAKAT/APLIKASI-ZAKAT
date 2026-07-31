from datetime import datetime

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

def zakat_fitrah(jiwa, harga):
    return jiwa * 2.5 * harga

def zakat_mal(harta):
    return 0.025 * harta

def now():
    return datetime.now().strftime("%Y-%m-%d")