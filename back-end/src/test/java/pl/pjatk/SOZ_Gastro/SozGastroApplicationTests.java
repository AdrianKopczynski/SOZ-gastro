package pl.pjatk.SOZ_Gastro;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import pl.pjatk.SOZ_Gastro.Exceptions.UserNotFoundException;
import pl.pjatk.SOZ_Gastro.ObjectClasses.User;
import pl.pjatk.SOZ_Gastro.Services.UserService;

@SpringBootTest
class SozGastroApplicationTests {

	@Autowired
	private UserService userService;
	@Test
	void contextLoads() {
	}

	@Test
	public void testGetUserById()
	{
		try {
			User user = userService.getById(1L);
			System.out.println("User found: " + user);
		} catch (UserNotFoundException e) {
			System.out.println("User not found");
		} catch (IllegalArgumentException e) {
			System.out.println("Invalid id: " + e.getMessage());
		}

	}


}
