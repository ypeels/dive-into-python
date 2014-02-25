"""Base class for creating HTML processing modules

This class is designed to take HTML as input and spit out equivalent
HTML as output.  By itself it's not very interesting; you use it by
subclassing it and providing the methods you need to create your HTML
transformation.

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

from sgmllib import SGMLParser                                                  # 8.2: sgmllib breaks HTML down into pieces
import htmlentitydefs                                                           # I guess this book predates standardized DOM?

class BaseHTMLProcessor(SGMLParser):                                            # 8.2: lists when fns are called
	def reset(self):                                                                # 8.4: SGMLParser base class is just a consumer.
		# extend (called by SGMLParser.__init__)                                         # BaseHTMLProcessor will also be a producer.
		self.pieces = []                                                        # 8.4: a (slower) alternative - pieces as an appendable string
		SGMLParser.reset(self)
		
	def unknown_starttag(self, tag, attrs):                                     # see section 8.4
		# called for each start tag
		# attrs is a list of (attr, value) tuples
		# e.g. for <pre class="screen">, tag="pre", attrs=[("class", "screen")]
		# Ideally we would like to reconstruct original tag and attributes, but
		# we may end up quoting attribute values that weren't quoted in the source
		# document, or we may change the type of quotes around the attribute value
		# (single to double quotes).
		# Note that improperly embedded non-HTML code (like client-side Javascript)
		# may be parsed incorrectly by the ancestor, causing runtime script errors.
		# All non-HTML code must be enclosed in HTML comment tags (<!-- code -->)
		# to ensure that it will pass through this parser unaltered (in handle_comment).
		strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs]) # takes attribute name/value pairs...
		self.pieces.append("<%(tag)s%(strattrs)s>" % locals())                  # reconstructs original HTML, and appends to pieces
                                                                                # 8.7: (nice) side effect is adding quotes to unquoted attribute values
	def unknown_endtag(self, tag):
		# called for each end tag, e.g. for </pre>, tag will be "pre"
		# Reconstruct the original end tag.
		self.pieces.append("</%(tag)s>" % locals())                             # 8.5: special function locals()! (also, globals())
                                                                                # returns dictionary of all local vars + values
	def handle_charref(self, ref):                                                  # 8.6: locals() "is the most common use of dictionary-based string formatting."
		# called for each character reference, e.g. for "&#160;", ref will be "160"     # but locals() also copies the local namespace, so beware the performance hit
		# Reconstruct the original character reference.
		self.pieces.append("&#%(ref)s;" % locals())                             # just reproducing the original &#<ref#>;
		
	def handle_entityref(self, ref):
		# called for each entity reference, e.g. for "&copy;", ref will be "copy"
		# Reconstruct the original entity reference.
		self.pieces.append("&%(ref)s" % locals())
		# standard HTML entities are closed with a semicolon; other entities are not
		if htmlentitydefs.entitydefs.has_key(ref):                              # special logic for non-standard HTML entities
			self.pieces.append(";")

	def handle_data(self, text):
		# called for each block of plain text, i.e. outside of any tag and
		# not containing any character or entity references
		# Store the original text verbatim.
		self.pieces.append(text)                                                # append plain text unaltered
		
	def handle_comment(self, text):
		# called for each HTML comment, e.g. <!-- insert Javascript code here -->
		# Reconstruct the original comment.
		# It is especially important that the source document enclose client-side
		# code (like Javascript) within comments so it can pass through this
		# processor undisturbed; see comments in unknown_starttag for details.
		self.pieces.append("<!--%(text)s-->" % locals())                        # wrap comments with comment delimiters
		
	def handle_pi(self, text):
		# called for each processing instruction, e.g. <?instruction>
		# Reconstruct original processing instruction.
		self.pieces.append("<?%(text)s>" % locals())                            # wrap instructions with instruction delimiters

	def handle_decl(self, text):
		# called for the DOCTYPE, if present, e.g.
		# <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		#	 "http://www.w3.org/TR/html4/loose.dtd">
		# Reconstruct original DOCTYPE
		self.pieces.append("<!%(text)s>" % locals())
		
	def output(self):                                                           # never called by SGMLParser
		"""Return processed HTML as a single string"""
		return "".join(self.pieces)                                             # "Python is great at lists and mediocre at strings" because the latter are immutable, hence inefficient to modify

if __name__ == "__main__":
	for k, v in globals().items():                                              # 8.5: special function globals() returns 
		print k, "=", v                                                         # a dictionary with all of this module's globals { "name": value }  

                                                                                # BEWARE!!! locals() is read-only, globals() is not!!!
                                                                                # see Example 8.12 in Section 8.5. locals() makes a copy of the local namespace...