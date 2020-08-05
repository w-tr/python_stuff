# Wesley Taylor 2014
# Program to parse xilinx bitfile header & do md5 checksum on the remainder
# Comparison done on the checksum generated
# To utilise. Run in idle. ignore reponse in console. type compare("bitfile1", "bitfile2")

import sys
import hashlib

def parse_bit(file):

  """A function to parse xilinx bit files, and seperate the bitstream from the header"""

  length = ord(next(file)) << 8 | ord(next(file))
  for i in range(length):
    next(file)
  length = ord(next(file)) << 8 | ord(next(file))

  fields = {}
  for i in "abcde":
    assert next(file) == i
    length = ord(next(file)) << 8 | ord(next(file))
    field = []
    for j in range(length):
      field.append(next(file))
    fields[i] = "".join(field)

  return fields, list(file)

def bit_report(filename, report):

  """Add bit file hash to a report"""

  file = open(filename).read()
  file = iter(file)
  file = parse_bit(file)

  report.heading("Bit File Report", 0)
  report.heading("Bit File Header", 1)
  report.preformatted(filename)

  table = [["Key", "Value"]]
  for i in "abcde":
    table.append([str(i), str(file[0][i])])
  report.tabulate(table)

  report.heading("Bit Stream", 1)

  hash = hashlib.md5()
  hash.update("".join(file[1]))
  hash = "".join(["%x"%ord(i) for i in hash.digest()])

  report.tabulate([
    ["length (bytes):", "sha1_hash"],
    [str(len(file[1])), hash],
  ])

def bit_compare_report(filename1, filename2, report):

  """Add bit file hash to a report"""

  report.heading("Bit File Comparison", 0)

  file = open(filename1).read()
  file = iter(file)
  file = parse_bit(file)

  report.heading("Original Header", 1)
  report.preformatted(filename1)

  table = [["Key", "Value"]]
  for i in "abcde":
    table.append([str(i), str(file[0][i])])
  report.tabulate(table)

  report.heading("Original Bitstream", 1)

  original_hash = hashlib.md5()
  original_hash.update("".join(file[1]))
  original_hash = "".join(["%x"%ord(i) for i in original_hash.digest()])

  report.tabulate([
    ["length (bytes):", "sha1_hash"],
    [str(len(file[1])), original_hash],
  ])

  file = open(filename2).read()
  file = iter(file)
  file = parse_bit(file)

  report.heading("Rebuilt Header", 1)
  report.preformatted(filename2)

  table = [["Key", "Value"]]
  for i in "abcde":
    table.append([str(i), str(file[0][i])])
  report.tabulate(table)

  report.heading("Rebuilt Bitstream", 1)

  hash = hashlib.md5()
  hash.update("".join(file[1]))
  hash = "".join(["%x"%ord(i) for i in hash.digest()])

  report.tabulate([
    ["length (bytes):", "sha1_hash"],
    [str(len(file[1])), hash],
  ])

  report.heading("Bitstream Comparison", 1)
  if hash == original_hash:
    report.paragraph("Rebuild successful.")
  else:
    report.paragraph("Rebuild **Fail** file did not match.")

def compare(file1, file2):

  """Compare only the bitstreams of 2 bit files, but print the headers"""

  original = file1
  original = open(original, "rb").read()
  original = iter(original)
  original = parse_bit(original)

  rebuild = file2
  rebuild = open(rebuild, "rb").read()
  rebuild = iter(rebuild)
  rebuild = parse_bit(rebuild)

  print "original header"
  print "===============\n"
  for i in "abcde":
    print i, original[0][i]

  print "\nrebuild header"
  print "===============\n"
  for i in "abcde":
    print i, rebuild[0][i]

  print "\noriginal bitstream"
  print "==================\n"
  print "length (bytes):", len(original[1])
  a = hashlib.md5()
  a.update("".join(original[1]))
  print "".join(["%x"%ord(i) for i in a.digest()])

  print "\nrebuild bitstream"
  print "==================\n"
  print "length (bytes):", len(rebuild[1])
  b = hashlib.md5()
  b.update("".join(rebuild[1]))
  print "".join(["%x"%ord(i) for i in b.digest()])

  if original[1] == rebuild[1]:
    print "\nbitstreams match"
    return True
  else:
    print "\nbitstreams differ"
    return False

if __name__ == "__main__":
  compare(sys.argv[1], sys.argv[2])
  
