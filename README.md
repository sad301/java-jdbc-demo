# Java JDBC Demo

Contoh program java dengan koneksi ke database MySQL

## Pembuatan Database

Langkah-langkah dibawah untuk dikerjakan menggunakan MySQL Client (Terminal/Command Prompt). Untuk phpMyAdmin atau aplikasi sejenis harap menyesuaikan

1. Login ke MySQL, kemudian ketika perintah dibawah untuk mendapatkan direktori yang diizinkan MySQL untuk import file CSV

    ```sql
    SHOW VARIABLES like 'secure_file_priv';
    ```
   
2. Copy file `people-100.csv` ke direktori yang disebutkan pada kolom `Value`, sebagai contoh: `C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\`
3. Buka file `people.sql`, edit baris `load data infile '/var/lib/mysql-files/people-100.csv'`. Sesuaikan direktori yang disebutkan dengan direktori yang anda gunakan, sebagai contoh :

    ```sql
    LOAD DATA INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\person-100.csv'
    ```

4. Jalankan *Command Prompt*, pindah ke direktori _project_, kemudian login ke MySQL. Dalam MySQL ketik perintah :

    ```sql
    SOURCE people.sql
    ```
   
## Kompilasi Project

Project ini menggunakan Maven, untuk kompilasi gunakan perintah :

```
mvn clean compile
```

Untuk non-maven, gunakan perintah berikut :

```
DIR /S /B src\*.java > sources.list
javac @sources.list -d target\classes
```

## Eksekusi Project

1. Buat folder `lib`
2. Download [MySQL Connector/J](https://dev.mysql.com/downloads/), ekstrak dan pindahkan file `mysql-connector-j-xyz.jar` ke dalam folder `lib`
3. Jalankan program menggunakan perintah :

```
java -cp lib\mysql-connector-j-xyz.jar;target\classes com.example.Main
```