package pl.pjatk.SOZ_Gastro.Services;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import pl.pjatk.SOZ_Gastro.Exceptions.UserNotFoundException;
import pl.pjatk.SOZ_Gastro.ObjectClasses.User;
import pl.pjatk.SOZ_Gastro.Repositories.UserRepository;
import pl.pjatk.SOZ_Gastro.Exceptions.BadRequestException;

import java.util.List;

@Service
public class UserService
{
    private final RestTemplate restTemplate;
    private final UserRepository userRepository;
    public UserService(RestTemplate restTemplate, UserRepository userRepository)
    {
        this.restTemplate = restTemplate;
        this.userRepository = userRepository;
    }

    public User createUser(Long id, User user) throws BadRequestException
    {
        if (id != null)
        {
            throw new BadRequestException();
        }
        else if (user.getId() != null)
        {
            throw new BadRequestException();
        }
        return userRepository.save(user);
    }
    public User getByUsername(String username) throws UserNotFoundException
    {
        if (username == null || username.trim().isEmpty())
        {
            throw new IllegalArgumentException("Username cannot be null or empty");
        }

        return this.userRepository.findByUsername(username).orElseThrow(UserNotFoundException::new);
    }

    public User getById(Long id) throws UserNotFoundException
    {
        if (id == null)
        {
            throw new IllegalArgumentException("Id cannot be null");
        }
        return this.userRepository.findById(id).orElseThrow(UserNotFoundException::new);
    }

    public List<User>  getAll(){return this.userRepository.findAll();}

}
