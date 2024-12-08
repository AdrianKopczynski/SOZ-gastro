package pl.pjatk.SOZ_Gastro.Controller;

import org.apache.coyote.BadRequestException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pl.pjatk.SOZ_Gastro.ObjectClasses.User;
import pl.pjatk.SOZ_Gastro.Services.UserService;

import java.util.List;

@RestController
@RequestMapping("User")
public class UserController
{

    private final UserService userService;

    public UserController(UserService userService)
    {
        this.userService = userService;
    }

    @GetMapping("/allUsers")
    public ResponseEntity<List<User>> getAll()
    {
        return ResponseEntity.ok().body(this.userService.getAll());
    }
    //you can't declare id while creating a new user
    @PostMapping(value = {"", "/{id}"})
    public ResponseEntity<User> createUser(@PathVariable(required = false) Long id, @RequestBody User data){
        return ResponseEntity.ok().body(this.userService.createUser(id, data));
    }
}
