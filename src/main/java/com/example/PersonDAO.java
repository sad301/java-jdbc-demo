package com.example;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class PersonDAO {

  private final Connection connection;

  public PersonDAO(Connection connection) {
    this.connection = connection;
  }

  public int create(Person person) throws SQLException {
    String sql = "";
    PreparedStatement ps = connection.prepareStatement(sql);
    return 0;
  }

  public List<Person> retrieve() throws SQLException {
    List<Person> rows = new ArrayList<>();
    String sql = "SELECT * FROM person";
    PreparedStatement ps = connection.prepareStatement(sql);
    ResultSet rs = ps.executeQuery();
    while (rs.next()) {
      Person person = new Person();
      person.setId(rs.getInt("id"));
      person.setUserId(rs.getString("user_id"));
      person.setFirstName(rs.getString("first_name"));
      person.setLastName(rs.getString("last_name"));
      person.setSex(rs.getString("sex"));
      person.setEmail(rs.getString("email"));
      person.setPhone(rs.getString("phone"));
      person.setBirthDate(LocalDate.parse("birth_date"));
      rows.add(person);
    }
    rs.close();
    return rows;
  }

  public int delete(Person person) throws SQLException {
    String sql = "";
    PreparedStatement ps = connection.prepareStatement(sql);
    return 0;
  }

  public int update(Person person) throws SQLException {
    String sql = "";
    PreparedStatement ps = connection.prepareStatement(sql);
    return 0;
  }
}
