# train_siamese.py

import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.model_selection import train_test_split
from src.ml_core.training import SiameseTrainer
from src.ml_core.data.data_utils import create_pairs_from_data

# --- CONFIGURACIÓN ---
print("TensorFlow Version:", tf.__version__)

IMG_SIZE = (128, 128)
IMG_SHAPE = (128, 128, 1)
BATCH_SIZE = 128
EPOCHS = 50
MODEL_SAVE_DIR = "ml_models"
MODEL_SAVE_PATH = os.path.join(MODEL_SAVE_DIR, "base_handwriting_model.keras")
DATASET_DIR = "dataset/variations"

def main():
    print("\nVerificando disponibilidad de GPU...")
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"GPU detectada: {len(gpus)} dispositivo(s) físico(s)")
        except RuntimeError as e: print(e)
    else:
        print("ADVERTENCIA: No se detectó ninguna GPU. El entrenamiento será en CPU.")

    print("\n=== PASO 1: CARGANDO DATASET CON TF.DATA (RÁPIDO) ===")
    full_dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR, label_mode='int', color_mode='grayscale', image_size=IMG_SIZE,
        batch_size=1024,
        shuffle=False
    ).unbatch()

    print("Convirtiendo dataset a arrays de NumPy en memoria...")
    images_list, labels_list = [], []
    for image, label in full_dataset:
        images_list.append(image.numpy())
        labels_list.append(label.numpy())
    
    all_images = np.array(images_list, dtype="float32") / 255.0
    all_labels = np.array(labels_list, dtype="int32")
    print(f"Carga completa: {len(all_images)} imágenes.")

    train_images, val_images, train_labels, val_labels = train_test_split(
        all_images, all_labels, test_size=0.2, random_state=42, stratify=all_labels
    )
    
    print("\n=== PASO 2: CREANDO PARES DE ÍNDICES ===")
    train_pairs_idx, train_pair_labels = create_pairs_from_data(train_images, train_labels)
    val_pairs_idx, val_pair_labels = create_pairs_from_data(val_images, val_labels)

    print("\n=== PASO 3: CONSTRUYENDO PIPELINE DE DATOS EN MEMORIA ===")
    def generator(pair_indices, pair_labels, image_data):
        def gen():
            for (idx_a, idx_b), label in zip(pair_indices, pair_labels):
                yield (image_data[idx_a], image_data[idx_b]), label
        return gen

    output_signature = (
        (tf.TensorSpec(shape=IMG_SHAPE, dtype=tf.float32), tf.TensorSpec(shape=IMG_SHAPE, dtype=tf.float32)),
        tf.TensorSpec(shape=(), dtype=tf.float32)
    )

    train_ds = tf.data.Dataset.from_generator(generator(train_pairs_idx, train_pair_labels, train_images), output_signature=output_signature)
    val_ds = tf.data.Dataset.from_generator(generator(val_pairs_idx, val_pair_labels, val_images), output_signature=output_signature)

    train_ds = train_ds.shuffle(len(train_pairs_idx)).batch(BATCH_SIZE).repeat().prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.batch(BATCH_SIZE).repeat().prefetch(tf.data.AUTOTUNE)

    print("\n=== PASO 4: ENTRENANDO MODELO ===")
    trainer = SiameseTrainer(
        img_shape=IMG_SHAPE, batch_size=BATCH_SIZE, epochs=EPOCHS,
        model_save_dir=MODEL_SAVE_DIR, model_save_path=MODEL_SAVE_PATH
    )
    
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(MODEL_SAVE_DIR, "best_model.keras"),
            monitor='val_siamese_contrastive_accuracy', mode='max', save_best_only=True, verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7, verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_siamese_contrastive_accuracy', patience=5, verbose=1, mode='max', restore_best_weights=True
        )
    ]
    
    steps_per_epoch = len(train_pairs_idx) // BATCH_SIZE
    validation_steps = len(val_pairs_idx) // BATCH_SIZE

    # --- ¡CORRECCIÓN AQUÍ! ---
    # La función .fit() de Keras usa los argumentos que definimos dentro de la clase SiameseTrainer.
    # El método .train() dentro de la clase ahora llama a .fit() con la sintaxis correcta.
    # Necesitamos pasar los argumentos correctamente a nuestra función `train`.
    trainer.history = trainer.model.fit(
        train_ds,
        validation_data=val_ds, # La función .fit() SÍ espera 'validation_data'
        epochs=EPOCHS,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        callbacks=callbacks,
        verbose=1
    )
    trainer.model.save(trainer.model_save_path)


    print("\n=== PASO 5: VISUALIZANDO RESULTADOS ===")
    trainer.plot_training_history(save_path='training_history_final.png', show=True)

if __name__ == "__main__":
    main()