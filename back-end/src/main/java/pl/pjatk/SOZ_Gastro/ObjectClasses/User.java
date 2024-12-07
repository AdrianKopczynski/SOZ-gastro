package pl.pjatk.SOZ_Gastro.ObjectClasses;

import jakarta.persistence.*;
import pl.pjatk.SOZ_Gastro.Enums.UserType;

@Entity
@Table(name="user")
public class User extends Meal {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String username;
    private String password;
    private boolean enabled;
    @Column(name = "user_type", columnDefinition = "enum('Admin', 'Inventory', 'Cashier' ")
    @Enumerated(EnumType.STRING)
    private UserType userType;

    public User(Integer id, String username, String loginPin, UserType userType, boolean enabled)
    {
        this.id = id;
        this.username = username;
        this.password = loginPin;
        this.userType = userType;
        this.enabled = enabled;
    }
    public User(){}

    public void setId(Integer id) {
        this.id = id;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getPassword() {
        return password;
    }

    public Integer getId() {
        return id;
    }

    public UserType getUserType() {
        return userType;
    }

    public String getUsername() {
        return username;
    }

    public void setUserType(UserType userType) {
        this.userType = userType;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public boolean isEnabled() {
        return enabled;
    }
}