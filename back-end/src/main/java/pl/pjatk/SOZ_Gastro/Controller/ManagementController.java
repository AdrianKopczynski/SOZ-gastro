package pl.pjatk.SOZ_Gastro.Controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pl.pjatk.SOZ_Gastro.Services.ManagementService;

@RestController
@RequestMapping("Management")
public class ManagementController {
    private final ManagementService managementService;

    public ManagementController(ManagementService coreService){this.managementService = coreService;}

    @GetMapping("/hello")
    public ResponseEntity<String> hello(@RequestParam(required=false)  String pin ){
        return ResponseEntity.ok(managementService.helloWorld()+pin);
    }

    @PostMapping("/log")
    public ResponseEntity<String> login(@RequestParam String pin){
        return ResponseEntity.ok(managementService.helloWorld()+pin);
    }
}
