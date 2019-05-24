/**
 * @package    AcyMailing for Joomla!
 * @version    5.10.4
 * @author     acyba.com
 * @copyright  (C) 2009-2018 ACYBA S.A.R.L. All rights reserved.
 * @license    GNU/GPLv3 http://www.gnu.org/licenses/gpl-3.0.html
 */

var task, formName;

function submitacymailingform(newtask, newformName) {
	task = newtask;
	formName = newformName;

	var recaptchaid = 'acymailing-captcha';
	if(newformName) recaptchaid = newformName+'-captcha';

	var invisibleRecaptcha = document.querySelector('#'+recaptchaid+'[class="g-recaptcha"][data-size="invisible"]');
	if(invisibleRecaptcha && typeof grecaptcha == "object"){

		var grcID = invisibleRecaptcha.getAttribute('grcID');

		if(!grcID) {
			grcID = grecaptcha.render(recaptchaid, {
				'sitekey': invisibleRecaptcha.getAttribute("data-sitekey"),
				'callback': 'acySubmitSubForm',
				'size': 'invisible',
				'expired-callback': 'resetRecaptcha'
			});

			invisibleRecaptcha.setAttribute('grcID', grcID);
		}

		var response = grecaptcha.getResponse(grcID);
		if(response){
			return acySubmitSubForm();
		}else{
			grecaptcha.execute(grcID);
			return false;
		}
	}else{
		return acySubmitSubForm();
	}
}

function resetRecaptcha(){
	var recaptchaid = 'acymailing-captcha';
	if(formName) recaptchaid = formName+'-captcha';

	var invisibleRecaptcha = document.querySelector('#'+recaptchaid+'[class="g-recaptcha"][data-size="invisible"]');
	if(!invisibleRecaptcha) return;

	var grcID = invisibleRecaptcha.getAttribute('grcID');
	grecaptcha.reset(grcID);
}

function acySubmitSubForm(){
	var varform = document[formName];
	if(typeof acymailingModule != 'undefined') {
		var filterEmail = acymailingModule['emailRegex'];
	}else{
		var filterEmail = /\@/i;
	}

	if(!varform.elements){
		if(varform[0].elements['user[email]'] && varform[0].elements['user[email]'].value && filterEmail.test(varform[0].elements['user[email]'].value)){
			varform = varform[0];
		}else{
			varform = varform[varform.length - 1];
		}
	}

	if(task != 'optout'){
		nameField = varform.elements['user[name]'];
		if(nameField && typeof acymailingModule != 'undefined' && (typeof acymailingModule['reqFields' + formName] != 'undefined' && acymailingModule['reqFields' + formName].indexOf('name') >= 0 && ((nameField.value == acymailingModule['NAMECAPTION'] || (typeof acymailingModule['excludeValues' + formName] != 'undefined' && typeof acymailingModule['excludeValues' + formName]['name'] != 'undefined' && nameField.value == acymailingModule['excludeValues' + formName]['name'])) || nameField.value.replace(/ /g, "").length < 2))){
			alert(acymailingModule['NAME_MISSING']);
			nameField.className = nameField.className + ' invalid';
			return false;
		}
	}

	var emailField = varform.elements['user[email]'];
	if(emailField){
		if(typeof acymailingModule == 'undefined' || emailField.value != acymailingModule['EMAILCAPTION']) emailField.value = emailField.value.replace(/ /g, "");
		if(!emailField || (typeof acymailingModule != 'undefined' && (emailField.value == acymailingModule['EMAILCAPTION'] || (typeof acymailingModule['excludeValues' + formName] != 'undefined' && typeof acymailingModule['excludeValues' + formName]['email'] != 'undefined' && emailField.value == acymailingModule['excludeValues' + formName]['email']))) || !filterEmail.test(emailField.value)){
			if(typeof acymailingModule != 'undefined'){
				alert(acymailingModule['VALID_EMAIL']);
			}
			emailField.className = emailField.className + ' invalid';
			return false;
		}
	}

	if(varform.elements['hiddenlists'].value.length < 1){
		var listschecked = false;
		var alllists = varform.elements['subscription[]'];
		if(alllists && (typeof alllists.value == 'undefined' || alllists.value.length == 0)){
			for(b = 0; b < alllists.length; b++){
				if(alllists[b].checked) listschecked = true;
			}
			if(!listschecked){
				alert(acymailingModule['NO_LIST_SELECTED']);
				return false;
			}
		}
	}

	if(task != 'optout' && typeof acymailingModule != 'undefined'){
		if(typeof acymailingModule['reqFields' + formName] != 'undefined' && acymailingModule['reqFields' + formName].length > 0){

			for(var i = 0; i < acymailingModule['reqFields' + formName].length; i++){
				elementName = 'user[' + acymailingModule['reqFields' + formName][i] + ']';
				elementToCheck = varform.elements[elementName];
				if(elementToCheck){
					var isValid = false;
					if(typeof elementToCheck.value != 'undefined'){
						if(elementToCheck.value == ' ' && typeof varform[elementName + '[]'] != 'undefined'){
							if(varform[elementName + '[]'].checked){
								isValid = true;
							}else{
								for(var a = 0; a < varform[elementName + '[]'].length; a++){
									if((varform[elementName + '[]'][a].checked || varform[elementName + '[]'][a].selected) && varform[elementName + '[]'][a].value.length > 0) isValid = true;
								}
							}
						}else{
							if(elementToCheck.value.replace(/ /g, "").length > 0){
								if(typeof acymailingModule['excludeValues' + formName] == 'undefined' || typeof acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] == 'undefined' || acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] != elementToCheck.value) isValid = true;
							}
						}
					}else{
						for(var a = 0; a < elementToCheck.length; a++){
							if(elementToCheck[a].checked && elementToCheck[a].value.length > 0) isValid = true;
						}
					}
					if((elementToCheck.length >= 1 && (elementToCheck[0].parentElement.parentElement.style.display == 'none' || elementToCheck[0].parentElement.parentElement.parentElement.style.display == 'none')) || (typeof elementToCheck.length == 'undefined' && (elementToCheck.parentElement.parentElement.style.display == 'none' || elementToCheck.parentElement.parentElement.parentElement.style.display == 'none'))){
						isValid = true;
					}
					if(!isValid){
						elementToCheck.className = elementToCheck.className + ' invalid';
						alert(acymailingModule['validFields' + formName][i]);
						return false;
					}
				}else{
					if((varform.elements[elementName + '[day]'] && varform.elements[elementName + '[day]'].value < 1) || (varform.elements[elementName + '[month]'] && varform.elements[elementName + '[month]'].value < 1) || (varform.elements[elementName + '[year]'] && varform.elements[elementName + '[year]'].value < 1902)){
						if(varform.elements[elementName + '[day]'] && varform.elements[elementName + '[day]'].value < 1) varform.elements[elementName + '[day]'].className = varform.elements[elementName + '[day]'].className + ' invalid';
						if(varform.elements[elementName + '[month]'] && varform.elements[elementName + '[month]'].value < 1) varform.elements[elementName + '[month]'].className = varform.elements[elementName + '[month]'].className + ' invalid';
						if(varform.elements[elementName + '[year]'] && varform.elements[elementName + '[year]'].value < 1902) varform.elements[elementName + '[year]'].className = varform.elements[elementName + '[year]'].className + ' invalid';
						alert(acymailingModule['validFields' + formName][i]);
						return false;
					}

					if((varform.elements[elementName + '[country]'] && varform.elements[elementName + '[country]'].value < 1) || (varform.elements[elementName + '[num]'] && (varform.elements[elementName + '[num]'].value < 3 || (typeof acymailingModule['excludeValues' + formName] != 'undefined' && typeof acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] != 'undefined' && acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] == varform.elements[elementName + '[num]'].value)))){
						if((varform.elements[elementName + '[country]'] && varform.elements[elementName + '[country]'].parentElement.parentElement.style.display != 'none') || (varform.elements[elementName + '[num]'] && varform.elements[elementName + '[num]'].parentElement.parentElement.style.display != 'none')){
							if(varform.elements[elementName + '[country]'] && varform.elements[elementName + '[country]'].value < 1) varform.elements[elementName + '[country]'].className = varform.elements[elementName + '[country]'].className + ' invalid';
							if(varform.elements[elementName + '[num]'] && (varform.elements[elementName + '[num]'].value < 3 || (typeof acymailingModule['excludeValues' + formName] != 'undefined' && typeof acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] != 'undefined' && acymailingModule['excludeValues' + formName][acymailingModule['reqFields' + formName][i]] == varform.elements[elementName + '[num]'].value))) varform.elements[elementName + '[num]'].className = varform.elements[elementName + '[num]'].className + ' invalid';
							alert(acymailingModule['validFields' + formName][i]);
							return false;
						}
					}
				}
			}
		}

		if(typeof acymailingModule != 'undefined' && typeof acymailingModule['checkFields' + formName] != 'undefined' && acymailingModule['checkFields' + formName].length > 0){
			for(var i = 0; i < acymailingModule['checkFields' + formName].length; i++){
				elementName = 'user[' + acymailingModule['checkFields' + formName][i] + ']';
				elementtypeToCheck = acymailingModule['checkFieldsType' + formName][i];
				elementToCheck = varform.elements[elementName].value;
				if(typeof acymailingModule['excludeValues' + formName] != 'undefined'){
					var excludedValues = acymailingModule['excludeValues' + formName][acymailingModule['checkFields' + formName][i]];
					if(typeof excludedValues != 'undefined' && elementToCheck == excludedValues){
						continue;
					}
				}
				switch(elementtypeToCheck){
					case 'number':
						myregexp = new RegExp('^[0-9]*$');
						break;
					case 'letter':
						myregexp = new RegExp('^[A-Za-z\u00C0-\u017F ]*$');
						break;
					case 'letnum':
						myregexp = new RegExp('^[0-9a-zA-Z\u00C0-\u017F ]*$');
						break;
					case 'regexp':
						myregexp = new RegExp(acymailingModule['checkFieldsRegexp' + formName][i]);
						break;
				}
				if(!myregexp.test(elementToCheck)){
					alert(acymailingModule['validCheckFields' + formName][i]);
					return false;
				}
			}
		}
	}

	var captchaField = varform.elements['acycaptcha'];
	if(captchaField){
		if(captchaField.value.length < 1){
			if(typeof acymailingModule != 'undefined'){
				alert(acymailingModule['CAPTCHA_MISSING']);
			}
			captchaField.className = captchaField.className + ' invalid';
			return false;
		}
	}

	if(task != 'optout'){
		var termsandconditions = varform.terms;
		if(termsandconditions && !termsandconditions.checked){
			if(typeof acymailingModule != 'undefined'){
				alert(acymailingModule['ACCEPT_TERMS']);
			}
			termsandconditions.className = termsandconditions.className + ' invalid';
			return false;
		}

		if(typeof acymailingModule != 'undefined' && typeof acymailingModule['excludeValues' + formName] != 'undefined'){
			for(var fieldName in acymailingModule['excludeValues' + formName]){
				if(!acymailingModule['excludeValues' + formName].hasOwnProperty(fieldName)) continue;
				if(!varform.elements['user[' + fieldName + ']'] || varform.elements['user[' + fieldName + ']'].value != acymailingModule['excludeValues' + formName][fieldName]) continue;

				varform.elements['user[' + fieldName + ']'].value = '';
			}
		}
	}

	if(typeof ga != 'undefined' && task != 'optout'){
		ga('send', 'pageview', 'subscribe');
	}else if(typeof ga != 'undefined'){
		ga('send', 'pageview', 'unsubscribe');
	}

	taskField = varform.task;
	taskField.value = task;

	if(!varform.elements['ajax'] || !varform.elements['ajax'].value || varform.elements['ajax'].value == '0'){
		varform.submit();
		return false;
	}

	var form = document.getElementById(formName);

	var formData = new FormData(form);
	form.className += ' acymailing_module_loading';
	form.style.filter = "alpha(opacity=50)";
	form.style.opacity = "0.5";

	var xhr = new XMLHttpRequest();
	xhr.open('POST', form.action);
	xhr.onload = function(){
		var message = 'Ajax Request Failure';
		var type = 'error';

		if (xhr.status === 200){
			var response = JSON.parse(xhr.responseText);
			message = response.message;
			type = response.type;
		}
		acymailingDisplayAjaxResponse(decodeURIComponent(message), type, formName);
	};
	xhr.send(formData);

	return false;
}

function acymailingDisplayAjaxResponse(message, type, formName){
	var toggleButton = document.getElementById('acymailing_togglemodule_' + formName);

	if(toggleButton && toggleButton.className.indexOf('acyactive') > -1){
		var wrapper = toggleButton.parentElement.parentElement.childNodes[1];
		wrapper.style.height = '';
	}

	var responseContainer = document.querySelectorAll('#acymailing_fulldiv_' + formName + ' .responseContainer')[0];

	if(typeof responseContainer == 'undefined'){
		responseContainer = document.createElement('div');
		var fulldiv = document.getElementById('acymailing_fulldiv_' + formName);

		if(fulldiv.firstChild){
			fulldiv.insertBefore(responseContainer, fulldiv.firstChild);
		}else{
			fulldiv.appendChild(responseContainer);
		}
		
		oldContainerHeight = '0px';
	}else{
		oldContainerHeight = responseContainer.style.height;
	}

	responseContainer.className = 'responseContainer';

	var form = document.getElementById(formName);

	var elclass = form.className;
	var rmclass = 'acymailing_module_loading';
	var res = elclass.replace(' '+rmclass, '', elclass);
	if(res == elclass) res = elclass.replace(rmclass+' ', '', elclass);
	if(res == elclass) res = elclass.replace(rmclass, '', elclass);
	form.className = res;

	responseContainer.innerHTML = message;

	if(type == 'success'){
		responseContainer.className += ' acymailing_module_success';
	}else{
		responseContainer.className += ' acymailing_module_error';
		form.style.opacity = "1";
	}

	newContainerHeight = responseContainer.style.height;

	form.style.display = 'none';
	responseContainer.className += ' slide_open';
}


