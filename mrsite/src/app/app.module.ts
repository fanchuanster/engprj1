import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MrComponent } from './mr/mr.component';
import { HttpClientModule } from '@angular/common/http';
import { MrService } from './mr.service';


@NgModule({
  declarations: [
    AppComponent,
    MrComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  exports: [
    MrComponent
  ],
  providers: [MrService],
  bootstrap: [AppComponent]
})
export class AppModule { }
