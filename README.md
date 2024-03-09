# Tubes1_Arctica-Kenapa-Batal

### bang kenapa entelect challenge 2022 (arctica) gak dilanjutin??? uE 😭 Ue 😭 Ue 🥹🥹 uE 😞😞UE 😭😭😭 UEEE 😢😢 UEEE 🥀🥀 Uue 😢😢 E 💧💧 UUE 😭😭 EEU 🥹 E 🥹 UE 💧 UUU 😭😭
![Screenshot](8ihg6a.jpg)
![Screenshot](noarcticamegamind.jpg)
![Screenshot](noarctica.jpg)

## Cara menjalankan bot 
1. Pastikan Anda sudah memiliki repository dari game engine yang tertera di bawah ini dan mengetahui cara mengaktivasi game engine tersebut (caranya sudah tertulis di repository tersebut juga)
   ```
   https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0  
   ```
2. Buka file ```main.py``` dan lakukan import bot di dalam file ```nearest.py``` dengan cara mengetik
   ```
   from game.logic.nearest import MeowNearestDiamond
   ```
   di bagian atas file ```main.py```
3. Perhatikan bagian ```CONTROLLERS = {}``` di file ```main.py```, untuk menambahkan kelas bot yang ada di repository ini, ketik
   ```
     "nama apa saja di sini, wajib tanpa spasi, ketik juga kedua tanda petik duanya" = MeowNearestDiamond
   ```
   di dalam kurung kurawal dalam ```CONTROLLERS = {}```.
4. Untuk menjalankan satu buah bot, ketik

    ```
    python main.py --logic <nama yang ditulis di bagian 3 tanpa tanda petik dua> --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

5. Untuk menjalankan beberapa bot dengan logic yang sama, ketik hal yang sama di bagian 4 ke dalam salah satu file di bawah ini (berdasarkan OS yang digunakan)

    Windows

    ```
    ./run-bots.bat
    ```

    Linux / mungkin macOS

    ```
    ./run-bots.sh
    ```

    <b>Sebelum mengeksekusi script di atas, pastikan untuk mengubah izin shell script agar bisa mengeksekusi script tersebut (untuk linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

#### Catatan:

-   Jika Anda menjalankan beberapa bot, pastikan email dan nama unik If you run multiple bots, make sure each emails and names are unique
-   Email bisa apa saja selama mengikuti format sintaks email yang benar
-   Nama dan password boleh apa saja selama tidak mengandung spasi
