/**
 * Simple Markdown to HTML Converter
 * Handles basic markdown formatting for QA portfolio
 */

function markdownToHtml(markdown) {
  let html = markdown;

  // Escape HTML first
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // Headings (# ## ### etc)
  html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

  // Code blocks (```language ... ```)
  html = html.replace(/```([a-z]*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Bold and italic
  html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/____(.*?)____/g, '<strong><em>$1</em></strong>');
  html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
  html = html.replace(/_(.*?)_/g, '<em>$1</em>');

  // Links [text](url)
  html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');

  // Lists - unordered
  html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/^\- (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*?<\/li>)/s, (match) => {
    if (!match.includes('<ul>')) {
      return '<ul>' + match + '</ul>';
    }
    return match;
  });

  // Lists - ordered
  html = html.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');

  // Horizontal rule
  html = html.replace(/^---$/gm, '<hr />');

  // Tables
  html = html.replace(/^\| (.*?) \|$/gm, (match) => {
    const cells = match.split('|').filter((cell) => cell.trim());
    return '<tr><td>' + cells.join('</td><td>') + '</td></tr>';
  });

  // Line breaks - paragraphs
  html = html.replace(/\n\n+/g, '</p><p>');
  html = '<p>' + html + '</p>';

  // Clean up excessive p tags around block elements
  html = html.replace(/<p><(h[1-6]|ul|ol|pre|blockquote|hr)/g, '<$1');
  html = html.replace(/<\/(h[1-6]|ul|ol|pre|blockquote|hr)><\/p>/g, '</$1>');

  // Blockquotes
  html = html.replace(/^&gt; (.*?)$/gm, '<blockquote>$1</blockquote>');

  // Unescape code blocks
  html = html.replace(/&lt;/g, (match, offset) => {
    if (html.substring(offset, offset + 6).includes('pre')) return match;
    return '<';
  });
  html = html.replace(/&gt;/g, (match, offset) => {
    if (html.substring(offset - 50, offset).includes('pre')) return match;
    return '>';
  });

  return html;
}

// Export for Node.js or browser usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { markdownToHtml };
}
