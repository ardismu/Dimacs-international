/**
*
* Copyright 2017 Google Inc. All rights reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

/**<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>*/
//flip1
		$(document).ready(function(){
			
//OServices
			//UserLogin more viewer
		 $("#showLogin").click(function(){
		 $("#LogInEmployer, #showEmployerR").hide();
		 $("#LogInUser").show();
		  });		
			
			//UserEmployer more viewer
		 $("#showEmployer").click(function(){
		 $("#LogInUser, #showLoginR").hide();
		 $("#LogInEmployer").show();
		  });			
			
//ABOUT US VIEWING
			//ITC more viewer
		 $("#showITC").click(function(){
		 $("#Mmodus,#BusOpp,#Trainer").hide();
		 $("#ITC").show();
		  });
			//Modus more viewer
		 $("#showMmodus").click(function(){
		 $("#ITC,#BusOpp,#Trainer").hide();
		 $("#Mmodus").show();
		  });
			//Business more viewer
		 $("#showBus").click(function(){
		 $("#ITC,#Mmodus,#Trainer").hide();
		 $("#BusOpp").show();
		  });
			//Training more viewer
		 $("#showTrainer").click(function(){
		 $("#ITC,#Mmodus,#BusOpp").hide();
		 $("#Trainer").show();

		  });
//image show
		  $("#fixedImg").mouseleave(function(){
			$("#fixedImg").hide();
		  });
		  $("#hideImg").click(function(){
			$("#fixedImg").hide();
		  });
		  $("#showImg").click(function(){
			$("#fixedImg").show();
		  });

//MESL Portfolio
		// $("#MESLPort").mouseleave(function(){
		//	$("#MESLPort").hide();
		//  });
		  $("#hideMESL").click(function(){
			$("#MESLPort").hide();
		  });
		  $("#showMESL").click(function(){
			$("#MESLPort").show();
		  });			
			
			
//show1
//		  $("#hide").click(function(){
		  $("#fixed").mouseleave(function(){
			$("#fixed").hide();
		  });
		  $("#show").click(function(){
			$("#fixed").show();
		  });
//show2
		  $("#hide2").click(function(){
			$("#fixed2").hide();
		  });
		  $("#show2").click(function(){
			$("#fixed2").show();
		  });
//show3
		  $("#hide3").click(function(){
			$("#fixed3").hide();
		  });
		  $("#show3").click(function(){
			$("#fixed3").show();
		  });
//show4
		  $("#hide4").click(function(){
			$("#fixed4").hide();
		  });
		  $("#show4").click(function(){
			$("#fixed4").show();
		  });
//show5
		  $("#hide5").click(function(){
			$("#fixed5").hide();
		  });
		  $("#show5").click(function(){
			$("#fixed5").show();
		  });
//show6
		  $("#hide6").click(function(){
			$("#fixed6").hide();
		  });
		  $("#show6").click(function(){
			$("#fixed6").show();
		  });
			
});