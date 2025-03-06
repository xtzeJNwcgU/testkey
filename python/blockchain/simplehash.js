function simpleHash(input) {
    // Konversi input menjadi string dan ambil panjangnya
    const str = input.toString();
    const length = str.length;

    // Inisialisasi variabel hash
    let hash = 0;

    // Proses hashing
    for (let i = 0; i < length; i++) {
        // Ambil karakter dan konversi ke kode ASCII
        const char = str.charCodeAt(i);
        
        // Operasi hashing sederhana: penjumlahan dan rotasi
        hash = (hash + char) << 5 | (hash + char) >>> 27; // Rotasi ke kiri
    }

    // Kembalikan hash dalam format heksadesimal
    return hash.toString(16);
}

// Contoh penggunaan
const input = "Hello, World!";
const hashValue = simpleHash(input);
console.log(`Hash dari "${input}" adalah: ${hashValue}`);