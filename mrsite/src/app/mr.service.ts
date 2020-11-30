import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MrService {

  constructor(private http: HttpClient) { }

  private recommendUrl = environment.api_url + '/recommend/';
  private movieTitlesUrl = environment.api_url + '/recommend/movie_titles';
    
  getRecommendations(title: string): Observable<string[]> {
    console.log(this.recommendUrl)
    return this.http.get<string[]>(this.recommendUrl + encodeURI(title));
  }

  getMovieTitles(): Observable<string[]> {
    return this.http.get<string[]>(this.movieTitlesUrl);
  }
}
