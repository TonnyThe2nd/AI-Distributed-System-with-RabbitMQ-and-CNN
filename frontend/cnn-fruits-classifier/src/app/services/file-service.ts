import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root',
})
export class FileService {

  private readonly apiUrl = 'http://localhost:8000/';

  constructor(private http: HttpClient) {}

  uploadFile(file: File) {
    const formData = new FormData();
    formData.append('files', file);
    return this.http.post(`${this.apiUrl}predict`, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }
}
