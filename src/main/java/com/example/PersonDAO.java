package com.example;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class PersonDAO {

  private final Connection connection;
  private final DateTimeFormatter fmt;
  private PreparedStatement psCreate, psRetrieve, psUpdate, psDelete;

  public PersonDAO(Connection connection) {
    this.connection = connection;
    fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
  }

  public void initialize() throws SQLException {
    psCreate = connection.prepareStatement("""
      INSERT INTO person (id, first_name, last_name, sex, email, phone, birth_date, job_title)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """);
    psRetrieve = connection.prepareStatement("SELECT * FROM person");
    psUpdate = connection.prepareStatement("""
      UPDATE person
      SET first_name = ?, last_name = ?, sex = ?, email = ?, phone = ?, birth_date = ?, job_title = ?
      WHERE id = ?
      """);
    psDelete = connection.prepareStatement("DELETE FROM person WHERE id = ?");
  }

  public int create(Person person) throws SQLException {
    psCreate.setString(1, person.getId());
    psCreate.setString(2, person.getFirstName());
    psCreate.setString(3, person.getLastName());
    psCreate.setString(4, person.getSex());
    psCreate.setString(5, person.getEmail());
    psCreate.setString(6, person.getPhone());
    psCreate.setString(7, person.getBirthDate().format(fmt));
    psCreate.setString(8, person.getJobTitle());
    return psCreate.executeUpdate();
  }

  public List<Person> retrieve() throws SQLException {
    List<Person> rows = new ArrayList<>();
    ResultSet rs = psRetrieve.executeQuery();
    while (rs.next()) {
      Person person = new Person();
      person.setId(rs.getString("id"));
      person.setFirstName(rs.getString("first_name"));
      person.setLastName(rs.getString("last_name"));
      person.setSex(rs.getString("sex"));
      person.setEmail(rs.getString("email"));
      person.setPhone(rs.getString("phone"));
      person.setBirthDate(LocalDate.parse(rs.getString("birth_date"), fmt));
      person.setJobTitle(rs.getString("job_title"));
      rows.add(person);
    }
    rs.close();
    return rows;
  }

  public int update(Person person) throws SQLException {
    psUpdate.setString(1, person.getFirstName());
    psUpdate.setString(2, person.getLastName());
    psUpdate.setString(3, person.getSex());
    psUpdate.setString(4, person.getEmail());
    psUpdate.setString(5, person.getPhone());
    psUpdate.setString(6, person.getBirthDate().format(fmt));
    psUpdate.setString(7, person.getJobTitle());
    psUpdate.setString(8, person.getId());
    return psUpdate.executeUpdate();
  }

  public int delete(Person person) throws SQLException {
    psDelete.setString(1, person.getId());
    return psDelete.executeUpdate();
  }

  public void close() throws SQLException {
    psCreate.close();
    psRetrieve.close();
    psUpdate.close();
  }
}
