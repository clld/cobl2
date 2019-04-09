<%inherit file="../home_comp.mako"/>

<%doc>
<%def name="sidebar()">
    <div class="well">
        <h3>Sidebar</h3>
        <p>
            Content
        </p>
    </div>
</%def>
</%doc>

<h2>Welcome to IE-CoR</h2>

<span style='font-size:120%'>a new breed of language databases on <strong>Co</strong>gnate <strong>R</strong>elationships in core vocabulary</em></span>

<p class="lead">

<h4>What are ‘<strong>Co</strong>gnate <strong>R</strong>elationships’?</h4>

<p>One basic way of assessing how closely certain languages are related to each other is through ‘cognacy’, i.e. to what extent they still share words that go back to the same origin or not.  English ‘salt’, German ‘Salz’ and French ‘sel’, for instance, are all cognates, i.e. related words that all go back to the same original source word, in those languages’ single common ancestor language (‘Proto-Indo-European’).  On the other hand, ‘black’, ‘schwarz’ and ‘noir’ all go back to different source words, because of shifts in which word is used to represent which meaning.</p>

<h4>The CoR Database System</h4>

<p>CoR is a new database structure for exploring the <strong>Co</strong>gnate <strong>R</strong>elationships between languages in their basic or &#8216;core&#8217; vocabulary.  The core vocabulary covered is a reference list of 170 basic and common word meanings, such as ‘one’, ‘water’, ‘black’, and so on.  CoR uses a new 170 meaning list, based on a combination and adaptation of three lists already widely used in linguistics:  the Swadesh lists (100 and 200), and the Leipzig-Jakarta list (100).  This combination has been heavily revised to optimise it for consistency in both lexeme determination, and cognacy determination within Indo-European.  All 170 meanings have also been precisely (re)defined. </p>

<p>CoR is tailored for qualitative as well as quantitative research purposes, and includes data-exploration websites to search the rich linguistic data covered:  cognate sets, orthography, morphology, phonemic and IPA phonetic transcriptions, and links to further sources.  </p>

<h4>IE-CoR:  for the <strong>I</strong>ndo-<strong>E</strong>uropean Language Family</h4>

<p>IE-CoR replaces and supersedes the ${h.external_link('http://ielex.mpi.nl/', label='IELex')} database by ${h.external_link('http://katalog.uu.se/empinfo/?id=N14-1084', label='Michael Dunn')} &#8212; as used in high-profile articles by ${h.external_link('http://dx.doi.org/10.1126/science.1219669', label='Bouckaert et al. 2012')} in <em>Science</em> and ${h.external_link('http://dx.doi.org/10.1353/lan.2015.0005', label='Chang et al. 2015')} in <em>Language</em>, for example.  </p>

<p>Data are compiled through the CoR data-entry website, by a consortium of branch experts across Indo-European, working together with cross-family cognacy specialists to assign cognate sets and sub-sets.  As languages are revised and entered, all branch experts will be identified in the ‘Authors’ section of the IE-CoR website, both primary authors and cross-validators.</p>

<p>All contributors work to a new and very explicit set of protocols for lexeme and cognacy determination, for the new, optimised IE-CoR reference meaning list of 170.  Effectively, all data are being entered anew by our 70+ language and branch experts, and cognate determinations fully referenced with respect to standard works in Indo-European linguistics.  Many new languages are also being added.</p>

<h4>Who We Are</h4>

<p>The main co-ordinators of IE-CoR are ${h.external_link('https://shh-mpg.academia.edu/PaulHeggarty', label='Paul Heggarty')} and ${h.external_link('https://www.shh.mpg.de/employees/44299/25522', label='Cormac Anderson')}, at the ${h.external_link('https://www.shh.mpg.de/DLCE-research-overview', label='Dept of Linguistic and Cultural Evolution')} at the ${h.external_link('https://www.shh.mpg.de/en', label='Max Planck Institute for the Science of Human History')} in Jena, Germany.</p>

<p>The website and underlying database structure originated in those programmed by ${h.external_link('http://katalog.uu.se/empinfo/?id=N14-1084', label='Michael Dunn')}, using his LEXdb system, but have been re-created, re-designed and very significantly expanded by ${h.external_link('https://github.com/runjak', label='Jakob Runge')} and <a href="https://www.shh.mpg.de/person/42541/25500">Hans-Jörg Bibiko</a>. </p>

<p>See also the current list of <a href="${request.route_url('contributors')}">contributing authors</a>.  </p>

<p>
% for a in main_contributors:
    <a href="${request.route_url('contributors')}/${a.id}">
        <img class="img-polaroid" src="${a.photo|n}" title="${a.name}"/>
    </a>
% endfor
</p>
