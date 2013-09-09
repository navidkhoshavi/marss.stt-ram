
/*
 * MARSSx86 : A Full System Computer-Architecture Simulator
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Copyright 2009 Avadh Patel <apatel@cs.binghamton.edu>
 * Copyright 2009 Furat Afram <fafram@cs.binghamton.edu>
 *
 */

#ifndef CACHE_LINES_H
#define CACHE_LINES_H

#include <logic.h>
#include <queue>

namespace Memory {

    struct CacheLine
    {
        W64 tag;
        /* This is a generic variable used by all caches to represent its
         * coherence state */
        W8 state;

      int lineRefreshCounter;
      int lineDecayInterval;
      W64 lineLastAccess;
      int lineRetentionTime;
      int predictState;
      int predictStateIndicator;

      void init(W64 tag_t, W64 lineLastAccess_t) {
            tag = tag_t;
            if (tag == (W64)-1) state = 0;
	    lineLastAccess = lineLastAccess_t;
	    predictState = 0;
      }

        void reset() {
            tag = -1;
            state = 0;
	    predictStateIndicator = 0;
	    predictState = 0;
        }

        void invalidate() { reset(); }

        void print(ostream& os) const {
            os << "Cacheline: tag[", (void*)tag, "] ";
            os << "state[", state, "] ";
        }
    };

    static inline ostream& operator <<(ostream& os, const CacheLine& line)
    {
        line.print(os);
        return os;
    }

    static inline ostream& operator ,(ostream& os, const CacheLine& line)
    {
        line.print(os);
        return os;
    }

    // A base struct to provide a pointer to CacheLines without any need
    // of a template
    struct CacheLinesBase
    {
        public:
            virtual void init()=0;
            virtual W64 tagOf(W64 address)=0;
            virtual int latency() const =0;
            virtual int write_latency() const =0;
            virtual int tag_latency() const =0;
            virtual CacheLine* probe(MemoryRequest *request)=0;
            virtual CacheLine* insert(MemoryRequest *request,
                    W64& oldTag)=0;
            virtual int invalidate(MemoryRequest *request)=0;
            virtual bool get_port(MemoryRequest *request)=0;
            virtual void print(ostream& os) const =0;
      virtual W64 refresh()=0;
            virtual int get_line_bits() const=0;
            virtual int get_access_latency() const=0;
            virtual int get_write_latency() const=0;
            virtual int get_tag_latency() const=0;
            virtual int get_cycle_time() const=0;
            virtual int get_tref() const=0;
			virtual int get_size() const=0;
			virtual int get_set_count() const=0;
			virtual int get_way_count() const=0;
			virtual int get_line_size() const=0;
    };

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
        class CacheLines : public CacheLinesBase,
        public AssociativeArray<W64, CacheLine, SET_COUNT,
        WAY_COUNT, LINE_SIZE>
    {
        private:
            int readPortUsed_[BANKS];
            int writePortUsed_[BANKS];
            int readPorts_[BANKS];
            int writePorts_[BANKS];
            W64 lastAccessCycle_[BANKS];
	    int refreshMode_;
	    std::queue<int> refreshPendingQueue_;

        public:
            typedef AssociativeArray<W64, CacheLine, SET_COUNT,
                    WAY_COUNT, LINE_SIZE> base_t;
            typedef FullyAssociativeArray<W64, CacheLine, WAY_COUNT,
                    NullAssociativeArrayStatisticsCollector<W64,
                    CacheLine> > Set;

            CacheLines(int readPorts, int writePorts, int refreshMode);
            void init();
            W64 tagOf(W64 address);
            int latency() const { return LATENCY; };
	    int write_latency() const { return WRITE_LATENCY; };
	    int tag_latency() const { return TAG_LATENCY; };
	    int cycle_time() const { return CYCLE_TIME; };
	    int tref() const { return TREF; };
            CacheLine* probe(MemoryRequest *request);
            CacheLine* insert(MemoryRequest *request, W64& oldTag);
            int invalidate(MemoryRequest *request);
            bool get_port(MemoryRequest *request);
            void print(ostream& os) const;
	    W64 refresh();

			/**
			 * @brief Get Cache Size
			 *
			 * @return Size of Cache in bytes
			 */
			int get_size() const {
				return (SET_COUNT * WAY_COUNT * LINE_SIZE);
			}

			/**
			 * @brief Get Number of Sets in Cache
			 *
			 * @return Sets in Cache
			 */
			int get_set_count() const {
				return SET_COUNT;
			}

			/**
			 * @brief Get Cache Lines per Set (Number of Ways)
			 *
			 * @return Number of Cache Lines in one Set
			 */
			int get_way_count() const {
				return WAY_COUNT;
			}

			/**
			 * @brief Get number of bytes in a cache line
			 *
			 * @return Number of bytes in Cache Line
			 */
			int get_line_size() const {
				return LINE_SIZE;
			}

            int get_line_bits() const {
                return log2(LINE_SIZE);
            }

            int get_access_latency() const {
                return LATENCY;
            }

	    int get_write_latency() const {
	      return WRITE_LATENCY;
	    }

	    int get_tag_latency() const {
	      return TAG_LATENCY;
	    }

	    int get_cycle_time() const {
	      return CYCLE_TIME;
	    }
	    
	    int get_tref() const {
	      return TREF;
	    }

    };

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
        static inline ostream& operator <<(ostream& os, const
					   CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>&
                cacheLines)
        {
            cacheLines.print(os);
            return os;
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
        static inline ostream& operator ,(ostream& os, const
					  CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>&
                cacheLines)
        {
            cacheLines.print(os);
            return os;
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::CacheLines(int readPorts, int writePorts, int refreshMode):refreshMode_(refreshMode)
    {
	for (int i = 0; i < BANKS; i++) {
	  readPorts_[i] = readPorts;
	  readPortUsed_[i] = 0;
	  writePorts_[i] = writePorts;
	  writePortUsed_[i] = 0;
	  lastAccessCycle_[i] = 0;
	}
    }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      void CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::init()
        {
            foreach(i, SET_COUNT) {
                Set &set = base_t::sets[i];
                foreach(j, WAY_COUNT) {
		  set.data[j].init(-1, sim_cycle);
                }
            }
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      W64 CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::tagOf(W64 address)
        {
            return floor(address, LINE_SIZE);
        }


    // Return true if valid line is found, else return false
    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      CacheLine* CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::probe(MemoryRequest *request)
        {
            W64 physAddress = request->get_physical_address();
            CacheLine *line = base_t::probe(physAddress);

            return line;
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      CacheLine* CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::insert(MemoryRequest *request, W64& oldTag)
        {
            W64 physAddress = request->get_physical_address();
            CacheLine *line = base_t::select(physAddress, oldTag);

            return line;
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      int CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::invalidate(MemoryRequest *request)
        {
            return base_t::invalidate(request->get_physical_address());
        }


    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      bool CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::get_port(MemoryRequest *request)
        {
            bool rc = false;

	    double unavailability = 0;
	    int GRANULARITY = 1000;
	    int refresh_point; // refresh point = granularity * (1 - unavailability);
	    int refresh_cycle; // refresh_cycle = sim_cycle % granularity - refresh_point;

	    // cache is partioned into banks by sets (not ways)
	    int increment; // for computing setID
	    int setID;
	    W64 accessAddrIndex = bits(request->get_physical_address(), log2(LINE_SIZE), log2(SET_COUNT));
	    int accessBankID = accessAddrIndex * BANKS / SET_COUNT;
	    W64 refreshAddrIndex;
	    int refreshBankID;
	    int subArrayID;
	    int SUB_ARRAY_COUNT = 1024;

	    // update cache ports
	    if (refreshMode_ == 2) { // NO_REFRESH
	      if (lastAccessCycle_[accessBankID] + CYCLE_TIME <= sim_cycle) {
		lastAccessCycle_[accessBankID] = sim_cycle;
		writePortUsed_[accessBankID] = 0;
		readPortUsed_[accessBankID] = 0;
	      }
	    }
	    else if (refreshMode_ == 3 || // PERIODIC
		     refreshMode_ == 4 || // EXTEND
		     refreshMode_ == 5) { // DYNAMIC_SKIP
	      
	      // get refresh point for periodic refresh
	      unavailability = (double) SUB_ARRAY_COUNT / TREF;
	      assert(unavailability < 1);
	      refresh_point = GRANULARITY * (1 - unavailability);

	      if (sim_cycle % GRANULARITY <= refresh_point) { // not refreshing
		if (lastAccessCycle_[accessBankID] + CYCLE_TIME <= sim_cycle) {
		  lastAccessCycle_[accessBankID] = sim_cycle;
		  writePortUsed_[accessBankID] = 0;
		  readPortUsed_[accessBankID] = 0;
		}
	      }
	      else { // refreshing
		// get the ID of the bank that is currently refreshing
		refresh_cycle = sim_cycle % GRANULARITY - refresh_point;
		increment = GRANULARITY - refresh_point;
		subArrayID = ((sim_cycle / GRANULARITY) * increment + refresh_cycle) % SUB_ARRAY_COUNT;
		refreshBankID = subArrayID * BANKS / SUB_ARRAY_COUNT;

		lastAccessCycle_[refreshBankID] = sim_cycle;
		writePortUsed_[refreshBankID] = 1;
		readPortUsed_[refreshBankID] = 1;

		if (accessBankID != refreshBankID) {
		  if (lastAccessCycle_[accessBankID] + CYCLE_TIME <= sim_cycle) {
		    lastAccessCycle_[accessBankID] = sim_cycle;
		    writePortUsed_[accessBankID] = 0;
		    readPortUsed_[accessBankID] = 0;
		  }
		}
	      }
	    } // else if (refreshMode_ == X)
	    else {
	      assert(0);
	    }

            switch(request->get_type()) {
                case MEMORY_OP_READ:
                    rc = (readPortUsed_[accessBankID] < readPorts_[accessBankID]) ? ++readPortUsed_[accessBankID] : 0;
                    break;
                case MEMORY_OP_WRITE:
		  // For an LLC, MEMORY_OP_WRITE is more like a read operation that loads to upper caches on hit
		  rc = (readPortUsed_[accessBankID] < readPorts_[accessBankID]) ? ++readPortUsed_[accessBankID] : 0;
		  break;
                case MEMORY_OP_UPDATE:
		  // MEMORY_OP_UPDATE = writeback from upper caches in the case of LLC
		  rc = (writePortUsed_[accessBankID] < writePorts_[accessBankID]) ? ++writePortUsed_[accessBankID] : 0;
		  break;
                case MEMORY_OP_EVICT:
                    rc = (writePortUsed_[accessBankID] < writePorts_[accessBankID]) ? ++writePortUsed_[accessBankID] : 0;
                    break;
                default:
                    memdebug("Unknown type of memory request: " <<
                            request->get_type() << endl);
                    assert(0);
            };
            return rc;
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      void CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::print(ostream& os) const
        {
            foreach(i, SET_COUNT) {
                const Set &set = base_t::sets[i];
                foreach(j, WAY_COUNT) {
                    os << set.data[j];
                }
            }
        }

    template <int SET_COUNT, int WAY_COUNT, int LINE_SIZE, int LATENCY, int WRITE_LATENCY, int TAG_LATENCY, int CYCLE_TIME, int TREF, int BANKS>
      W64 CacheLines<SET_COUNT, WAY_COUNT, LINE_SIZE, LATENCY, WRITE_LATENCY, TAG_LATENCY, CYCLE_TIME, TREF, BANKS>::refresh()
        {
	  double unavailability = 0;
	  int GRANULARITY = 1000;
	  int refresh_point;
	  int refresh_cycle;
	  int increment;
	  int setID;
	  int subArrayID;
	  int SUB_ARRAY_COUNT = 1024;
	  int SET_PER_SUBARRAY = SET_COUNT / SUB_ARRAY_COUNT;

	  W64 refresh_count = 0; // number of refresh operations

	  int max = 0; // for predictStateIndicator

	  // SRAM or STT-RAM
	  if (TREF == 0) {
	    if (refreshMode_ == 2) { // NO_REFRESH
	      refresh_count = 0;
	    }
	  }
	  // eDRAM
	  else {
	    if (refreshMode_ == 2 || // NO_REFRESH
		refreshMode_ == 3 || // PERIODIC
		refreshMode_ == 4 || // EXTEND
		refreshMode_ == 5) { // DYNAMIC_SKIP
	      unavailability = (double) SUB_ARRAY_COUNT / TREF;
	      refresh_point = GRANULARITY * (1 - unavailability);
	      refresh_cycle = sim_cycle % GRANULARITY - refresh_point;

	      // refresh region
	      if (sim_cycle % GRANULARITY >= refresh_point) {
		// which subarray to refresh
		increment = GRANULARITY - refresh_point;
		subArrayID = ((sim_cycle / GRANULARITY) * increment + refresh_cycle) % SUB_ARRAY_COUNT;

		foreach (i, SET_PER_SUBARRAY) {
		  setID = subArrayID * SET_PER_SUBARRAY + i;
		  Set &set = base_t::sets[setID];

		  switch (refreshMode_) {
		  case 2: // NO_REFRESH
		    foreach (j, WAY_COUNT) {
		      if (set.data[j].lineRefreshCounter == 0) { 
			set.data[j].state = 0; // line becomes invalid
		      }
		      else {
			set.data[j].lineRefreshCounter -= 1;
		      }
		    }
		    break;
		  case 3: // PERIODIC
		    foreach (j, WAY_COUNT) {
		      if (set.data[j].lineRefreshCounter == 0) {
			refresh_count += 1;
			set.data[j].lineRefreshCounter = set.data[j].lineRetentionTime;
		      }
		      else {
			set.data[j].lineRefreshCounter -= 1;
		      }
		    }
		    break;
		  case 4: // EXTEND
		    // the extend scheme is implemented in cacheController.cpp
		    foreach (j, WAY_COUNT) {
		      if (set.data[j].lineRefreshCounter == 0) {
			refresh_count += 1;
			set.data[j].lineRefreshCounter = set.data[j].lineRetentionTime;
		      }
		      else {
			set.data[j].lineRefreshCounter -= 1;
		      }
		    }
		    break;
		  case 5: // DYNAMIC_SKIP
		    // logically, predictStateIndicator is a per-setr indicator
		    // it uses 3 bits (0~6), where 6 means the predictors associate to the set are off
		    foreach (j, WAY_COUNT)
		      if (set.data[j].predictStateIndicator > max)
			max = set.data[j].predictStateIndicator;

		    foreach (j, WAY_COUNT)
		      set.data[j].predictStateIndicator = max;

		    // predictState transistions
		    foreach (j, WAY_COUNT) {
		      // valid = true && predictor = on
		      if (set.data[j].state != 0 && set.data[j].predictStateIndicator != 6) {
			if (set.data[j].lineRefreshCounter == 0)
			  set.data[j].lineDecayInterval += 1;

			if (set.data[j].lineDecayInterval == 256) { // let decay interval = 256 * retention time
			  switch (set.data[j].predictState) {
			  case 0: // live state
			    switch (set.data[0].predictStateIndicator) {
			    case 0: // false prediction = 0
			      set.data[j].predictState = 1;
			      break;
			    case 1: // false prediction = 1
			      set.data[j].predictState = 3;
			      break;
			    case 2: // false prediction = 2
			      set.data[j].predictState = 4;
			      break;
			    case 3: // false prediction = 3
			      set.data[j].predictState = 5;
			      break;
			    case 4: // false prediction = 4
			      set.data[j].predictState = 6;
			      break;
			    case 5: // false prediction = 5
			      set.data[j].predictState = 7;
			      break;
			    }
			    break;
			  case 1: // dead
			    set.data[j].predictState = 2;
			    break;
			  case 2: // disable
			    // do nothing
			    break;
			  case 3: // intermediate state
			    set.data[j].predictState = 1;
			    break;
			  case 4: // intermediate state
			    set.data[j].predictState = 3;
			    break;
			  case 5: // intermidiate state
			    set.data[j].predictState = 4;
			    break;
			  case 6: // intermediate state
			    set.data[j].predictState = 5;
			    break;
			  case 7: // intermediate state
			    set.data[j].predictState = 6;
			    break;
			  } // switch (set.data[j].predictState)
			  
			  set.data[j].lineDecayInterval = 0; // reset lineDecayInterval
			} // if (set.data[j].lineDecayInterval == 256)
		      } // if (set.data[j].state != 0 && set.data[j].predictStateIndicator != 6)
		      else {
			// if predictStateIndicator is off, line is always live
			set.data[j].predictState = 0;
		      }
		    } // predictState transistions

		    // manage refresh
		    foreach (j, WAY_COUNT) {
		      // only refresh if line is valid and is not disabled
		      if (set.data[j].state != 0 && set.data[j].predictState != 2) {
			if (set.data[j].lineRefreshCounter == 0) {
			  refresh_count += 1;
			  set.data[j].lineRefreshCounter = set.data[j].lineRetentionTime;
			}
			else {
			  set.data[j].lineRefreshCounter -= 1;
			}
		      }
		    } // manage refresh
		    break;
		  } // switch (refreshMode_)
		} // foreach (i, SET_PER_SUBARRAY) {
	      } // if (sim_cycle % granularity >= refresh_point) {
	    } // if (refreshMode_ == X)
	  } // else (eDRAM)

	  return refresh_count;
        }

};

#endif // CACHE_LINES_H
