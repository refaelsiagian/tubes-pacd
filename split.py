import os
import shutil
import random

random.seed(42)

base_dir = os.path.join("Dataset", "Daun")
classes = [
    "Bruguiera gymnorhiza",
    "Lumnitzera racemosa",
    "Rhizopora apiculata",
    "Rhizopora mucronata",
]
train_ratio = 0.8
use_augmented_for_train = (
    True  # Ubah ke False jika ingin memakai citra asli saja
)

for cls in classes:
  cls_path = os.path.join(base_dir, cls)
  if not os.path.exists(cls_path):
    continue

  # Ambil hanya file asli (di luar folder augmented)
  orig_files = [
      f
      for f in os.listdir(cls_path)
      if os.path.isfile(os.path.join(cls_path, f))
      and f.lower().endswith((".jpg", ".jpeg", ".png"))
  ]

  random.shuffle(orig_files)
  split_idx = int(len(orig_files) * train_ratio)
  train_orig = orig_files[:split_idx]
  test_orig = orig_files[split_idx:]

  train_dest = os.path.join(base_dir, "Data Latih", cls)
  test_dest = os.path.join(base_dir, "Data Uji", cls)
  os.makedirs(train_dest, exist_ok=True)
  os.makedirs(test_dest, exist_ok=True)

  # 1. Salin Data Uji (100% citra asli)
  for f in test_orig:
    shutil.copy2(os.path.join(cls_path, f), os.path.join(test_dest, f))

  # 2. Salin Data Latih (citra asli)
  train_prefixes = set()
  for f in train_orig:
    shutil.copy2(os.path.join(cls_path, f), os.path.join(train_dest, f))
    # Simpan nama dasar tanpa ekstensi, misal: "DSC_9478_small"
    train_prefixes.add(os.path.splitext(f)[0])

  # 3. Salin file augmented HANYA jika induknya masuk ke Data Latih
  aug_path = os.path.join(cls_path, "augmented")
  if use_augmented_for_train and os.path.exists(aug_path):
    for aug_f in os.listdir(aug_path):
      if any(aug_f.startswith(prefix) for prefix in train_prefixes):
        shutil.copy2(
            os.path.join(aug_path, aug_f), os.path.join(train_dest, aug_f)
        )

print("Pembagian dataset Daun selesai tanpa data leakage!")