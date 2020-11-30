import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { MrService } from '../mr.service';

@Component({
  selector: 'app-mr',
  templateUrl: './mr.component.html',
  styleUrls: ['./mr.component.css']
})

export class MrComponent {

  constructor(private mrService: MrService) { }

  movie_title = "Grumpier Old Men";
  recommendations;
  
  recommend() {
    this.mrService.getRecommendations(this.movie_title).subscribe((data:string[])=>{
      console.log(data);
      this.recommendations = data;
   }) 
  }
}
