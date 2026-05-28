import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { ChangeDetectorRef } from '@angular/core';
import { HttpEventType } from '@angular/common/http';
import { FileService } from "../services/file-service";

const MAX_FILE_SIZE_MB = 50;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];
const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png'];

interface PredictionResponse {
  classe: string;
  confianca: number;
}

@Component({
  selector: 'app-file-upload',
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    MatTooltipModule,
    MatProgressBarModule
  ],
  templateUrl: './file-upload.html',
  styleUrls: ['./file-upload.css']
})
export class FileUpload {
  dragOver = false;
  uploading = false;
  uploadProgress: number[] = [];
  isDarkTheme = false;
  selectedFiles: File[] = [];
  errors: string[] = [];
  filePredictions: PredictionResponse[] = [];
  private uploadSubscriptions: { index: number; subscription: any }[] = [];

  constructor(private cdr: ChangeDetectorRef, private fileService: FileService) {}

  private isValidImage(file: File): boolean {
    const isMimeValid = ALLOWED_IMAGE_TYPES.includes(file.type);
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
    const isExtValid = ALLOWED_EXTENSIONS.includes(fileExt);
    return isMimeValid && isExtValid;
  }

  getFileIcon(file: File): string {
    if (this.isValidImage(file)) return 'image';
    return 'insert_drive_file';
  }

  onFileSelected(event: any): void {
    if (this.uploading) {
      this.errors.push('Aguarde o upload terminar antes de selecionar novos arquivos.');
      return;
    }
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.addFiles(Array.from(input.files));
      input.value = '';
    }
  }

  clearFiles(): void {
    if (this.uploading) {
      this.uploadSubscriptions.forEach(item => item.subscription.unsubscribe());
      this.uploadSubscriptions = [];
      this.uploading = false;
    }
    this.selectedFiles = [];
    this.uploadProgress = [];
    this.filePredictions = [];
    this.errors = [];
    this.cdr.detectChanges();
  }

  uploadFiles() {
    if (this.uploading || this.selectedFiles.length === 0) return;

    this.uploading = true;
    this.uploadProgress = new Array(this.selectedFiles.length).fill(0);
    this.filePredictions = [];
    for (let i = 0; i < this.selectedFiles.length; i++) {
      this.filePredictions.push(null as any);
    }
    this.errors = [];
    let completedCount = 0;

    this.selectedFiles.forEach((file, index) => {
      const subscription = this.fileService.uploadFile(file).subscribe({
        next: (event) => {
          if (event.type === HttpEventType.UploadProgress) {
            const percentDone = event.total ? Math.round(100 * event.loaded / event.total) : 0;
            this.uploadProgress[index] = percentDone;
            this.cdr.markForCheck();
          } else if (event.type === HttpEventType.Response) {
            const response: any = event.body;
            const prediction: PredictionResponse = response.predictions[0].resultado;
            this.filePredictions[index] = prediction;
            this.uploadProgress[index] = 100;
            this.cdr.markForCheck();
            completedCount++;
            if (completedCount === this.selectedFiles.length) {
              this.uploading = false;
              this.uploadSubscriptions = [];
              this.cdr.markForCheck();
              console.log('Todos os uploads finalizados', this.filePredictions);
            }
          }
        },
        error: (err) => {
          this.errors.push(`Erro no upload de ${file.name}: ${err.message}`);
          this.uploadProgress[index] = -1;
          completedCount++;
          if (completedCount === this.selectedFiles.length) {
            this.uploading = false;
            this.uploadSubscriptions = [];
            this.cdr.markForCheck();
          }
        }
      });
      this.uploadSubscriptions.push({ index, subscription });
    });
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    if (!this.uploading) this.dragOver = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.dragOver = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.dragOver = false;
    if (this.uploading) {
      this.errors.push('Aguarde o upload terminar antes de adicionar novos arquivos.');
      return;
    }
    const files = event.dataTransfer?.files;
    if (files) {
      this.addFiles(Array.from(files));
    }
  }

  removeFile(index: number): void {
    if (this.uploading) return;
    this.selectedFiles.splice(index, 1);
    this.uploadProgress.splice(index, 1);
    this.filePredictions.splice(index, 1);
  }

  addFiles(files: File[]): void {
    if (this.uploading) return;

    const newErrors: string[] = [];
    const validFiles: File[] = [];

    for (const file of files) {
      if (file.size > MAX_FILE_SIZE_BYTES) {
        newErrors.push(`${file.name} excede o limite de ${MAX_FILE_SIZE_MB}MB.`);
        continue;
      }
      if (!this.isValidImage(file)) {
        newErrors.push(`${file.name} não é uma imagem válida. Apenas JPG, JPEG e PNG são aceitos.`);
        continue;
      }
      if (!this.selectedFiles.some(existing => existing.name === file.name && existing.size === file.size)) {
        validFiles.push(file);
      } else {
        newErrors.push(`${file.name} já foi adicionado.`);
      }
    }

    if (newErrors.length) {
      this.errors.push(...newErrors);
    }
    if (validFiles.length) {
      this.selectedFiles.push(...validFiles);
    }
  }

  toggleTheme(): void {
    this.isDarkTheme = !this.isDarkTheme;
  }

  clearErrors(): void {
    this.errors = [];
  }

  trackByFile(index: number, file: File): string {
    return `${file.name}-${file.size}-${file.lastModified}`;
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}