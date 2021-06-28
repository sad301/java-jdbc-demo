function _() {

	this.index = {
		init: () => {
			$('input[type="text"]').focus(e => {
				$(e.target).closest('.field').removeClass('error');
				if(e.target.id == 'txt-dokumen') {
					$('#btn-select-file').removeClass('negative');
				}
			});
			$('input[name="dokumen"]').change(e => {
				$('#txt-dokumen').val(e.target.files[0].name);
			});
			$('#btn-select-file').click(e => {
				e.preventDefault();
				$('input[name="dokumen"]').trigger('click');
			});
			$('#btn-send').click(e => {
				e.preventDefault();
				let nama = $('input[name="nama"]');
				let handphone = $('input[name="handphone"]');
				let dokumen = $('input[name="dokumen"]');
				if(nama.val() == '') {
					nama.closest('.field').addClass('error');
				}
				if(handphone.val() == '') {
					handphone.closest('.field').addClass('error');
				}
				if(dokumen.val() == '') {
					dokumen.closest('.field').addClass('error');
					dokumen.siblings('.ui.button').addClass('negative');
				}
				if(nama.val() == '' || handphone.val() == '' || dokumen.val() == '') return false;
				$('form').submit();
			});
		}
	};

}

_.q = function () {
	return new _();
};
