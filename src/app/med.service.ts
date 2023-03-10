import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
export interface Med {
  id: number;
  text: string;
}
@Injectable({
  providedIn: 'root'
})
export class MedService {
  constructor(private http: HttpClient) { }

  getMed(first: number, rows: number, searchPhrase: string) {
    return this.http.get<{data: Med[], total: number}>(`http://localhost:5000/load/med?first=${first}&rows=${rows}&phrase=${searchPhrase}`);
  }
}
