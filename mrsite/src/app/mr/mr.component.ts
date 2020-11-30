import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { MrService } from '../mr.service';

@Component({
  selector: 'app-mr',
  templateUrl: './mr.component.html',
  styleUrls: ['./mr.component.css']
})

export class MrComponent implements OnInit {

  constructor(private mrService: MrService) { }

  movie_titles
  movie_title = "Grumpier Old Men";
  recommendations;

  $cars = [
    {model : "Ford Mustang", color : "red"},
    {model : "Fiat 500", color : "white"},
    {model : "Volvo XC90", color : "black"}
  ];
  
  ngOnInit(): void {
    this.mrService.getMovieTitles().subscribe((data:string[])=>{
      this.movie_titles = data;
   }) 
  }

  recommend() {
    this.mrService.getRecommendations(this.movie_title).subscribe((data:string[])=>{
      console.log(data);
      this.recommendations = data;
   }) 
  }
}
