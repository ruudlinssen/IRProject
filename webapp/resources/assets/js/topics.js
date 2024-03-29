const topics = document.getElementsByClassName('js-topicName');
const papers = document.getElementsByClassName('js-paperTitle');
const authors = document.getElementsByClassName('js-authorTitle');

const nextPaperButton = document.querySelector('.js-nextPaperButton');

if(nextPaperButton !== null){

	const papersLength = Array.from(papers).length;
	const authorsLength = Array.from(authors).length;

	const previousPaperButton = document.querySelector('.js-prevPaperButton');
	const previousAuthorButton = document.querySelector('.js-prevAuthorButton');
	const nextAuthorButton = document.querySelector('.js-nextAuthorButton');

	if(authorsLength <= 10){

		nextAuthorButton.disabled = true;
	}

	if(papersLength <= 10){

		nextPaperButton.disabled = true;
	}

	nextPaperButton.addEventListener('click', () => {

		const nextStart = parseInt(nextPaperButton.dataset.nextStart);

		Array.from(papers).forEach((paper, index) => {

			paper.classList.add('Hidden');

			if(nextStart <= index && index < nextStart + 10){

				paper.classList.remove('Hidden');
			}
		});

		nextPaperButton.dataset.nextStart = nextStart + 10;
		previousPaperButton.dataset.nextStart = parseInt(previousPaperButton.dataset.nextStart) + 10;
		previousPaperButton.disabled = false;

		if(nextStart + 10 > papers.length){
			nextPaperButton.disabled = true;
		}
	});

	previousPaperButton.addEventListener('click', () => {

		const prevNextStart = parseInt(previousPaperButton.dataset.nextStart);
		const nextStart = parseInt(nextPaperButton.dataset.nextStart);

		Array.from(papers).forEach((paper, index) => {

			paper.classList.add('Hidden');

			if(prevNextStart <= index && index < prevNextStart + 10){

				paper.classList.remove('Hidden');
			}
		});

		nextPaperButton.dataset.nextStart = nextStart - 10;
		previousPaperButton.dataset.nextStart = prevNextStart - 10;
		nextPaperButton.disabled = false;

		if(prevNextStart - 10 < 0){

			previousPaperButton.disabled = true;
		}
	});

	nextAuthorButton.addEventListener('click', () => {

		const nextStart = parseInt(nextAuthorButton.dataset.nextStart);

		Array.from(authors).forEach((author, index) => {

			author.classList.add('Hidden');

			if(nextStart <= index && index < nextStart + 10){

				author.classList.remove('Hidden');
			}
		});

		nextAuthorButton.dataset.nextStart = nextStart + 10;
		previousAuthorButton.dataset.nextStart = parseInt(previousAuthorButton.dataset.nextStart) + 10;
		previousAuthorButton.disabled = false;

		if(nextStart + 10 > authorsLength){
			nextAuthorButton.disabled = true;
		}
	});

	previousAuthorButton.addEventListener('click', () => {

		const prevNextStart = parseInt(previousAuthorButton.dataset.nextStart);
		const nextStart = parseInt(nextAuthorButton.dataset.nextStart);

		Array.from(authors).forEach((author, index) => {

			author.classList.add('Hidden');

			if(prevNextStart <= index && index < prevNextStart + 10){

				author.classList.remove('Hidden');
			}
		});

		nextAuthorButton.dataset.nextStart = nextStart - 10;
		previousAuthorButton.dataset.nextStart = prevNextStart - 10;
		nextAuthorButton.disabled = false;

		if(prevNextStart - 10 < 0){

			previousAuthorButton.disabled = true;
		}
	});
}