import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class MrService {

  constructor(private http: HttpClient) { }

  private heroesUrl = 'http://127.0.0.1:5000/recommend/Waiting%20to%20Exhale';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

    
  getHeroes(): Observable<string[]> {
    return this.http.get<string[]>(this.heroesUrl);
  }
}
