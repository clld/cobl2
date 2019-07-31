<%inherit file="../home_comp.mako"/>

<h2>Welcome to IE-CoR &#8230;</h2>

<span style='font-size:110%'>&#8230; a new breed of language databases on <strong>Co</strong>gnate <strong>R</strong>elationships across language families, implemented here in the first instance to the <strong>I</strong>ndo-<strong>E</strong>uropean language family.</span>

<h4>What are <strong>Co</strong>gnate <strong>R</strong>elationships?</h4>

<p>One basic way of assessing how closely certain languages are related to each other is through ‘cognacy’, i.e. to what extent they still share words that go back to the same origin.  English <em>salt</em>, German <em>Salz</em> and French <em>sel</em>, for instance, are all cognates, i.e. related words that all go back to the same original source word (<em>*sal-</em>), in those languages’ single common ancestor language (‘Proto-Indo-European’).  On the other hand, <em>black</em>, <em>schwarz</em> and <em>noir</em> all go back to different source words, because of shifts in which word is used to represent which meaning.</p>

<h4>The IE-CoR Database System</h4>

<p>CoR is a new database structure for exploring how languages relate to each other, in whether they still use cognate words in their ‘core’ vocabulary.  The ‘core’ vocabulary referred to is a set of common and basic word meanings, such as ‘one’, ‘water’, ‘black’, ‘drink’, and so on.  IE-CoR uses a new ‘Jena 170’ meaning set, based on a combination of three sets already widely used in linguistics:  the Swadesh 100-meaning set, the Swadesh 200-meaning set, and the Leipzig-Jakarta 100-meaning set (they overlap heavily with each other, but not entirely).  These three were combined, adapted and above all optimised to ensure the consistent data set. </p>

<p>CoR is tailored for qualitative as well as quantitative research purposes, and includes data-exploration websites to search the rich linguistic data covered:  cognate sets, orthography, morphology, phonemic and IPA phonetic transcriptions, full citation of all cognate sets at the Indo-European level, and links to further resources.  </p>

<h4>IE-CoR:  for the <strong>I</strong>ndo-<strong>E</strong>uropean language family</h4>

<p>CoR is a database structure model that can be extended to any language family.  It is applied first here to the Indo-European language family, as IE-CoR.  It succeeds and aspires to supersede the ${h.external_link('http://ielex.mpi.nl/', label='IELex')} database by ${h.external_link('http://katalog.uu.se/empinfo/?id=N14-1084', label='Michael Dunn')} &#8212; as used in high-profile and controversial articles by ${h.external_link('http://dx.doi.org/10.1126/science.1219669', label='Bouckaert et al. 2012')} in <em>Science</em> and ${h.external_link('http://dx.doi.org/10.1353/lan.2015.0005', label='Chang et al. 2015')} in <em>Language</em>, for example.  </p>

<p>Data are compiled through the ‘CoR online database creation system’, by a consortium of language and branch experts across the Indo-European family, working together with cross-family cognacy specialists to determine cognate status.  </p>

<p>All contributors have worked to a new and very explicit set of ${h.external_link('https://github.com/lingdb/CoBL/wiki/01--Policy-on-Selecting-Lexemes', label='protocols')} for lexeme determination in each language, and for cognacy determination, for the optimised IE-CoR set of 170 precisely (re)defined reference meanings.  The language data have effectively been entered entirely anew, and do not continue from previous databases (which had high rates of data errors and inconsistency).  IE-CoR also includes many new languages not covered by previous cognate databases for Indo-European.</p>

<h4>Who We Are</h4>

<p>The main authors of IE-CoR are ${h.external_link('https://shh-mpg.academia.edu/PaulHeggarty', label='Paul Heggarty')}, ${h.external_link('https://www.shh.mpg.de/employees/44299/25522', label='Cormac Anderson')} and ${h.external_link('https://shh-mpg.academia.edu/MatthewScarborough', label='Matthew Scarborough')}, at the ${h.external_link('https://www.shh.mpg.de/DLCE-research-overview', label='Dept of Linguistic and Cultural Evolution')} at the ${h.external_link('https://www.shh.mpg.de/en', label='Max Planck Institute for the Science of Human History')} in Jena, Germany.</p>

<p>CoR was designed by Heggarty and Anderson, who also designed the data collection methodology, and (especially Anderson) coordinated the linguistic coding team for IE-CoR.  Scarborough oversaw all determinations of cognacy at the deep Indo-European level.</p>

<p>The website and underlying database structure originated in the LEXdb system programmed by ${h.external_link('http://katalog.uu.se/empinfo/?id=N14-1084', label='Michael Dunn')}, but for IE-CoR have been entirely re-designed, re-programmed and hugely expanded by ${h.external_link('https://github.com/runjak', label='Jakob Runge')} and ${h.external_link('https://www.shh.mpg.de/person/42541/25500', label='Hans-Jörg Bibiko')}. </p>

<p>See also the current list of <a href="${request.route_url('contributors')}">contributing authors</a>.</p>
