package pl.pjatk.SOZ_Gastro.Controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Category;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Meal;
import pl.pjatk.SOZ_Gastro.ObjectClasses.Tabletop;
import pl.pjatk.SOZ_Gastro.Services.ManagementService;

import java.util.List;

@RestController
@RequestMapping("/management")
public class ManagementController {
    private final ManagementService managementService;

    public ManagementController(ManagementService managementService){this.managementService = managementService;}

    @GetMapping("/hello")
    public ResponseEntity<String> hello(@RequestParam(required=false)  String pin ){
        return ResponseEntity.ok(managementService.helloWorld()+pin);
    }

    @PostMapping("/log")
    public ResponseEntity<String> login(@RequestParam String pin){
        return ResponseEntity.ok(managementService.helloWorld()+pin);
    }

    @PostMapping("/addCategory")
    public ResponseEntity<Category> addCategory(@RequestBody Category category){
        return ResponseEntity.ok(managementService.addCategory(category));
    }

    @GetMapping("/getCategoryList")
    public ResponseEntity<List<Category>> getCategoryList(){
        return ResponseEntity.ok(managementService.getCategoryList());
    }

    @PostMapping("/addMeal")
    public ResponseEntity<Meal> addMeal(@RequestBody Meal meal){
        return ResponseEntity.ok(managementService.addMeal(meal));
    }
    @GetMapping("/getMealList")
    public ResponseEntity<List<Meal>> getMealList(){
        return ResponseEntity.ok(managementService.getMealList());
    }

    @PostMapping("/addTabletop")
    public ResponseEntity<Tabletop> addTabletop(@RequestBody Tabletop tabletop){
        return ResponseEntity.ok(managementService.addTabletop(tabletop));
    }
}
