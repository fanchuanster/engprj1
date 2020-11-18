import { Component, OnInit } from '@angular/core';
import { MrService } from '../mr.service';

@Component({
  selector: 'app-mr',
  templateUrl: './mr.component.html',
  styleUrls: ['./mr.component.css']
})

export class MrComponent implements OnInit {

  constructor(private mrService: MrService) { }

  ngOnInit(): void {
  }

  public movie_title: string = "Go with wind"
  public recommendations: string[] = ['xxx']
  
  recommend() {    
    this.recommendations = ['data', 'data 2'];
    this.mrService.getHeroes().subscribe((data:string[])=>{
      console.log(data);
      this.recommendations = ['data', 'data 2'];
   }) 
  }
}
