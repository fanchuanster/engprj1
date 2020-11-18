import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-mr',
  templateUrl: './mr.component.html',
  styleUrls: ['./mr.component.css']
})
export class MrComponent implements OnInit {

  ngOnInit(): void {
  }

  movie_title = "Go with wind"
  recommendations = ["none"]
  
  recommend() {
    this.movie_title = "xxx"
    this.recommendations = ['movie1', "movie2", "movie n"]
  }
}
