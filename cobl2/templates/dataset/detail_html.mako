<%inherit file="../home_comp.mako"/>

<h3>Welcome to IE-CoR &#8230;</h3>

<p>Please click for a <strong>${h.external_link('https://www.science.org/stoken/author-tokens/ST-1344/full', label='free download of our paper in Science')}</strong>. (permitted link, provided by <em>Science</em>).
<br />
Once on the <em>Science</em> page, click on the <strong>red pdf icon</strong>, to the right under the article title.</p>

<p>&nbsp;&nbsp;<em><strong>Language trees with sampled ancestors support a hybrid model for the origin of Indo-European languages</strong></em>.</p>

<p>&nbsp;&nbsp;Heggarty et al. (2023) &nbsp;—&nbsp; doi: 10.1126/science.abg0818 &nbsp;—&nbsp; supplement on <em>Science</em> ${h.external_link('https://www.science.org/action/downloadSupplement?doi=10.1126%2Fscience.abg0818&file=science.abg0818_sm.pdf', label='here')}.</p>

<p>The phylogenetic analyses and results reported in that paper are based on the IE-CoR database that you can now explore here.</p>
<p>&nbsp;</p>
<h4>What is IE-CoR?</h4>

<p>IE-CoR is a new breed of language databases on <strong>Co</strong>gnate <strong>R</strong>elationships across language families, implemented here in the first instance to the <strong>I</strong>ndo-<strong>E</strong>uropean language family.</p>

<p>The IE-CoR database and the protocols followed in drawing it up are set out extensively in the free online ${h.external_link('https://www.science.org/action/downloadSupplement?doi=10.1126%2Fscience.abg0818&file=science.abg0818_sm.pdf', label='supplementary information')}, especially section 3.</p>

<p>The logic behind this new IE-CoR database, and a comparison with previous databases, are set out in ${h.external_link('https://www.annualreviews.org/doi/10.1146/annurev-linguistics-011619-030507', label='Cognacy Databases and Phylogenetic Research on Indo-European')}.</p>

<p>&nbsp;</p>
<h4>What are <strong>Co</strong>gnate <strong>R</strong>elationships?</h4>

<p>One basic way of assessing how closely certain languages are related to each other is through ‘cognacy’, i.e. to what extent they still share words that go back to the same origin. English <em>salt</em>, German <em>Salz</em> and French <em>sel</em>, for instance, are all cognates, i.e. related words that all go back to the same original source word (<em>*sal-</em>), in those languages’ single common ancestor language (‘Proto-Indo-European’). On the other hand, <em>black</em>, <em>schwarz</em> and <em>noir</em> all go back to different source words, because of shifts in which word is used to represent which meaning.</p>

<p>&nbsp;</p>
<h4>The IE-CoR Database System</h4>

<p>IE-CoR uses a new database structure for exploring how languages relate to each other, in whether they still use cognate words in their ‘core’ vocabulary. The ‘core’ vocabulary referred to is a set of common and basic word meanings, such as ‘one’, ‘water’, ‘black’, ‘drink’, and so on. IE-CoR uses a new ‘Jena 170’ meaning set, based on a combination of three sets already widely used in linguistics: the Swadesh 100-meaning set, the Swadesh 200-meaning set, and the Leipzig-Jakarta 100-meaning set. These three were combined, adapted and above all optimised to ensure the most consistent data-set. </p>

<p>IE-CoR is tailored for qualitative as well as quantitative research purposes, and this data-exploration website allows users to search the rich linguistic data covered: cognate sets, orthography, morphology, phonemic and IPA phonetic transcriptions. It provides full citation of all cognate sets at the Indo-European level, and links to further resources.</p>

<p>&nbsp;</p>
<h4>IE-CoR: for the <strong>I</strong>ndo-<strong>E</strong>uropean language family</h4>

<p>The database structure model in IE-CoR can be extended to any language family. It is applied first here to the Indo-European language family, as IE-CoR. It succeeds and aspires to supersede the IELex database used in high-profile and controversial articles by ${h.external_link('http://dx.doi.org/10.1126/science.1219669', label='Bouckaert et al. 2012')} in <em>Science</em> and ${h.external_link('http://dx.doi.org/10.1353/lan.2015.0005', label='Chang et al. 2015')} in <em>Language</em>, for example.</p>

<p>Data were compiled through our online database creation system (CoBL), by a consortium of language and branch experts across the Indo-European family, working together with cross-family cognacy specialists to determine cognate status.</p>

<p>All contributors have worked to a new and very explicit set of protocols (see sections 3.5 and 3.6 ${h.external_link('https://www.science.org/action/downloadSupplement?doi=10.1126%2Fscience.abg0818&file=science.abg0818_sm.pdf', label='here')}) for lexeme determination in each language, and for cognacy determination, for the optimised IE-CoR set of 170 precisely (re)defined reference meanings. The language data have effectively been entered entirely anew, and do not continue from previous databases (which had high rates of data errors and inconsistency). IE-CoR also includes many new languages not covered by previous cognate databases for Indo-European.</p>

<p>&nbsp;</p>
<h4>Who We Are</h4>

<p>The main authors of IE-CoR are ${h.external_link('https://shh-mpg.academia.edu/PaulHeggarty', label='Paul Heggarty')}, ${h.external_link('https://shh-mpg.academia.edu/CormacAnderson', label='Cormac Anderson')} and ${h.external_link('https://shh-mpg.academia.edu/MatthewScarborough', label='Matthew Scarborough')}, while based at the ${h.external_link('https://www.eva.mpg.de/linguistic-and-cultural-evolution', label='Dept of Linguistic and Cultural Evolution')}, initially at the former Max Planck Institute for the Science of Human History in Jena, Germany, in 2021 relocated to the ${h.external_link('https://www.eva.mpg.de', label='Max Planck Institute for the Evolutionary Anthropology')} in Leipzig, Germany.</p>

<p>IE-CoR was designed by Heggarty and Anderson, who also designed the data collection methodology, and (especially Anderson) coordinated the linguistic coding team for IE-CoR. Scarborough oversaw all determinations of cognacy at the deep Indo-European level.</p>

<p>The website and underlying database structure originated in the LEXdb system programmed by ${h.external_link('http://katalog.uu.se/empinfo/?id=N14-1084', label='Michael Dunn')}, but for IE-CoR have been entirely re-designed, re-programmed and hugely expanded by ${h.external_link('https://github.com/runjak', label='Jakob Runge')} and ${h.external_link('https://www.eva.mpg.de/linguistic-and-cultural-evolution/staff/hans-joerg-bibiko/', label='Hans-Jörg Bibiko')}. </p>

<p>The data for individual languages were provided by our many <a href="${request.route_url('contributors')}">contributing authors</a>.</p>

<p>&nbsp;</p>
<h4>Sources and How to Cite</h4>

<p>Drawing up IE-CoR entailed two main tasks of linguistic analysis.</p>

<ol>
<li><p><strong>Lexeme determination</strong>: establishing, individually for each language, which exact lexeme represents that language’s primary term for the precise IE-CoR definition of the target sense of each of our 170 reference meanings, and in the target register (click on the &#8216;IE-CoR Definition&#8217; link immediately under the map on any IE-CoR meaning page, e.g. for the meaning <a href="${request.route_url('parameters')}/fire">FIRE</a>). Given these precise specifications, lexeme determination cannot be reliably extracted from a bilingual dictionary as a source, but requires extensive linguistic expertise in the language concerned. This is why IE-CoR looked to over 80 specialists to perform lexeme determinations for the languages in which they have expertise. The IE-CoR data for an individual language constitutes a new primary source in and of itself, authored by the language expert(s) who made those determinations. Each individual language page includes a ‘How to Cite’ link, with those language experts’ names as authors. (Secondary sources like dictionaries will often have been consulted, where necessary, but the final lexeme determination is on the authority of that expert.)</p></li>
<li><p><strong>Cognacy determination</strong>: establishing, separately for each individual IE-CoR reference meaning, which of the (primary!) lexemes in different languages belong to the same cognate set, i.e. derive from the same source word by direct descent (not borrowing). In most cases, especially all 1600+ cognate sets that <a href="${request.route_url('cognatesets')}?sSearch_3=Proto-Indo-European">go back to Proto-Indo-European</a>, these cognacy determinations are supported by multiple citations of leading works in Indo-European linguistics, not least <a href="${request.route_url('sources')}/141">LIV²</a> and <a href="${request.route_url('sources')}/274">NIL</a>. This referencing was performed in consultation among various specialists in the IE-CoR team, especially by ${h.external_link('https://shh-mpg.academia.edu/MatthewScarborough', label='Matthew Scarborough')} at the Indo-European level, and with other experts at the level of individual major branches, e.g. by ${h.external_link('https://ajp.academia.edu/Lechos%C5%82awJocz', label='Lechosław Jocz')} for the Slavic branch.</p></li>
</ol>

<p>For full details on the IE-CoR protocols for lexeme and cognate determination, see respectively sections 3.5 and 3.6 of the ${h.external_link('https://www.science.org/action/downloadSupplement?doi=10.1126%2Fscience.abg0818&file=science.abg0818_sm.pdf', label='supplementary information')} to the article Heggarty et al. (2023) in <em>Science</em> (see download link above).</p>
