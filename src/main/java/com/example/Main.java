package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Scanner;

/**
 * Hello world!
 */
public class Main {

    private final Connection conn;
    private final Scanner sc;
    private PersonDAO dao;

    public Main(Connection conn, Scanner sc) {
        this.conn = conn;
        this.sc = sc;
    }

    public void start() throws SQLException {
        System.out.println("Java JDBC Demo");
        dao = new PersonDAO(conn);
        dao.initialize();
        boolean loop = true;
        while (loop) {
            System.out.print("\n[create/retrieve/update/delete/exit]> ");
            String cmd = sc.nextLine().toLowerCase();
            switch (cmd) {
                case "create" -> create();
                case "retrieve" -> retrieve();
                case "update" -> update();
                case "delete" -> delete();
                case "exit" -> loop = false;
            }
        }
        System.out.println("\n> Thank You !");
    }

    private void create() {
        System.out.println("\n> Create Person");
        System.out.print("> Insert Id: ");
        String id = sc.nextLine();
        System.out.print("> Insert First Name: ");
        String firstName = sc.nextLine();
        System.out.print("> Insert Last Name: ");
        String lastName = sc.nextLine();
        System.out.print("> Insert Sex: ");
        String sex = sc.nextLine();
        System.out.print("> Insert Email: ");
        String email = sc.nextLine();
        System.out.print("> Insert Phone: ");
        String phone = sc.nextLine();
        System.out.print("> Insert Birth Date (yyyy-MM-dd): ");
        String birthDateStr = sc.nextLine();
        System.out.print("> Insert Job Title: ");
        String jobTitle = sc.nextLine();

        Person person = new Person();
        person.setId(id);
        person.setFirstName(firstName);
        person.setLastName(lastName);
        person.setSex(sex);
        person.setEmail(email);
        person.setPhone(phone);
        person.setJobTitle(jobTitle);

        try {
            person.setBirthDate(java.time.LocalDate.parse(birthDateStr));
            int rows = dao.create(person);
            System.out.println("> Created " + rows + " person(s).");
        } catch (java.time.format.DateTimeParseException e) {
            System.out.println("> Invalid date format. Please use yyyy-MM-dd.");
        } catch (java.sql.SQLException e) {
            System.out.println("> Database error: " + e.getMessage());
        }
    }

    private void retrieve() {
        System.out.println("\n> Retrieve Persons");
        try {
            java.util.List<Person> persons = dao.retrieve();
            if (persons.isEmpty()) {
                System.out.println("> No persons found.");
            } else {
                for (Person p : persons) {
                    System.out.printf("> %s %s (ID: %s, Sex: %s, Email: %s, Phone: %s, Job: %s, DOB: %s)\n",
                            p.getFirstName(), p.getLastName(), p.getId(), p.getSex(),
                            p.getEmail(), p.getPhone(), p.getJobTitle(), p.getBirthDate());
                }
            }
        } catch (java.sql.SQLException e) {
            System.out.println("> Database error: " + e.getMessage());
        }
    }

    private void update() {

        System.out.println("\n> Update Person");
        System.out.print("> Insert Id to update: ");
        String id = sc.nextLine();
        System.out.print("> Insert New First Name: ");
        String firstName = sc.nextLine();
        System.out.print("> Insert New Last Name: ");
        String lastName = sc.nextLine();
        System.out.print("> Insert New Sex: ");
        String sex = sc.nextLine();
        System.out.print("> Insert New Email: ");
        String email = sc.nextLine();
        System.out.print("> Insert New Phone: ");
        String phone = sc.nextLine();
        System.out.print("> Insert New Birth Date (yyyy-MM-dd): ");
        String birthDateStr = sc.nextLine();
        System.out.print("> Insert New Job Title: ");
        String jobTitle = sc.nextLine();

        Person person = new Person();
        person.setId(id);
        person.setFirstName(firstName);
        person.setLastName(lastName);
        person.setSex(sex);
        person.setEmail(email);
        person.setPhone(phone);
        person.setJobTitle(jobTitle);

        try {
            person.setBirthDate(java.time.LocalDate.parse(birthDateStr));
            int rows = dao.update(person);
            System.out.println("> Updated " + rows + " person(s).");
        } catch (java.time.format.DateTimeParseException e) {
            System.out.println("> Invalid date format. Please use yyyy-MM-dd.");
        } catch (java.sql.SQLException e) {
            System.out.println("> Database error: " + e.getMessage());
        }
    }

    private void delete() {
        System.out.println("\n> Delete Person");
        System.out.print("> Insert Id to delete: ");
        String id = sc.nextLine();
        
        Person person = new Person();
        person.setId(id);
        
        try {
            int rows = dao.delete(person);
            System.out.println("> Deleted " + rows + " person(s).");
        } catch (java.sql.SQLException e) {
            System.out.println("> Database error: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws SQLException {
        String url = "jdbc:mysql://localhost:3306/people";
        String user = "dev";
        String password = "inipassword";
        Connection c = DriverManager.getConnection(url, user, password);
        Scanner sc = new Scanner(System.in);
        Main main = new Main(c, sc);
        main.start();
    }
}
