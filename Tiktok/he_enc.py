# Mã Hóa Bởi Anhcode
# Tele: https://t.me/anhcodeclick
# KHÔNG THỂ GIẢI MÃ - ĐỪNG CỐ GẮNG VÔ ÍCH

import marshal, zlib, base64
exec(marshal.loads(zlib.decompress(base64.b64decode(b'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'))))