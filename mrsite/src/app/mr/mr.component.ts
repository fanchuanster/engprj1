import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { MrService } from '../mr.service';
import { ViewChild, ElementRef, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-mr',
  templateUrl: './mr.component.html',
  styleUrls: ['./mr.component.css']
})

export class MrComponent implements OnInit {

  constructor(private mrService: MrService) { }

  movie_titles
  movie_title = "Thor";
  recommendations;
  timeOutDuration = 1;
  timeOut;
  selectedDevice;
  ngOnInit(): void {
    
  }

  recommend() {
    this.mrService.getRecommendations(this.movie_title).subscribe((data:string[])=>{
      console.log(data);
      this.recommendations = data;
   }) 
  }

  name = 'Angular 4';
  origItems = [];
  @ViewChild('selectList', { static: false }) selectList: ElementRef;

  filterItem(event){
    if (typeof event !== 'string') {
      return;
    }

    var searchValue = event;
    this.movie_title = searchValue;
    if (searchValue == '') {
      this.movie_titles = [];
      return;
    }

    clearTimeout(this.timeOut);
    this.timeOut = setTimeout(() => {
      console.log('get ' + searchValue);
      this.mrService.getMovieTitles(searchValue).subscribe((data:string[])=>{
            this.movie_titles = data;
      })
    }, this.timeOutDuration);

      console.log(this.movie_titles.length);
      this.selectList.nativeElement.size = this.movie_titles.length + 1 ;       
   }
}

