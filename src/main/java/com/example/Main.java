package com.example;

import java.sql.Connection;
import java.util.Scanner;

/**
 * Hello world!
 */
public class Main implements Runnable {

    private final Connection conn;
    private final Scanner sc;

    public Main(Connection conn, Scanner sc) {
        this.conn = conn;
        this.sc = sc;
    }

    @Override
    public void run() {
        boolean stop = false;
        while (!stop) {
            System.out.print("> ");
            String cmd = sc.nextLine();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Main main = new Main(null, sc);
        Thread t = new Thread(main);
        t.start();
    }
}
