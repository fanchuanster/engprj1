import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MrComponent } from './mr/mr.component';


@NgModule({
  declarations: [
    AppComponent,
    MrComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
  ],
  exports: [
    MrComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
