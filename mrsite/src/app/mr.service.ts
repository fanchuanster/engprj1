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

  private heroesUrl = environment.api_url + '/recommend/';
    
  getRecommendations(title: string): Observable<string[]> {
    console.log(this.heroesUrl)
    return this.http.get<string[]>(this.heroesUrl + encodeURI(title));
  }
}
