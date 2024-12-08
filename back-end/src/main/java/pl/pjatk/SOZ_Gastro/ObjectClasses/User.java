package pl.pjatk.SOZ_Gastro.ObjectClasses;

import jakarta.persistence.*;
import pl.pjatk.SOZ_Gastro.Enums.UserType;

@Entity
@Table(name="user")
public class User extends Meal {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String loginPin;
    private boolean enabled;
    @Column(name = "user_type", columnDefinition = "enum('Admin', 'Inventory', 'Cashier' ")
    @Enumerated(EnumType.STRING)
    private UserType userType;

    public User(Long id, String username, String loginPin, UserType userType, boolean enabled)
    {
        this.id = id;
        this.username = username;
        this.loginPin = loginPin;
        this.userType = userType;
        this.enabled = enabled;
    }
    public User(){}

    public void setId(Long id) {
        this.id = id;
    }

    public void setLoginPin(String loginPin) {
        this.loginPin = loginPin;
    }

    public String getLoginPin() {
        return loginPin;
    }

    public Long getId() {
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

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}