package pl.pjatk.SOZ_Gastro.Services;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Category;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Meal;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Tabletop;
import pl.pjatk.SOZ_Gastro.Repositories.CategoryRepository;
import pl.pjatk.SOZ_Gastro.Repositories.MealRepository;
import pl.pjatk.SOZ_Gastro.Repositories.TabletopRepository;

import java.util.List;

//put table, put meal, put category

@Service
public class ManagementService {

    private final CategoryRepository categoryRepository;
    private final MealRepository mealRepository;
    private final TabletopRepository tabletopRepository;

    public ManagementService(CategoryRepository categoryRepository, MealRepository mealRepository, TabletopRepository tabletopRepository){

        this.categoryRepository=categoryRepository;
        this.mealRepository = mealRepository;
        this.tabletopRepository = tabletopRepository;
    }
    public String helloWorld(){return "Hello";}

    public Category addCategory (Category category){
        if (categoryRepository.existsByName(category.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "category with name" + category.getName() + "already exists");
        }
        return categoryRepository.save(category);
    }

    public List<Category> getCategoryList(){
        return categoryRepository.findAllByIdIsNotNull();
    }
    public Meal addMeal (Meal meal){
        return  mealRepository.save((meal));
    }

    public List<Meal> getMealList(){
        return mealRepository.findAllByIdIsNotNull();
    }

    public Tabletop addTabletop(Tabletop tabletop){
        return tabletopRepository.save(tabletop);
    }

}
