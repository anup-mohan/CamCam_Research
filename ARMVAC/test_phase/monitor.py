import sys
import psutil
import collections
import datetime
import time


class Monitor(object):

    def __init__(self):
        self.start_timestamp = time.time()
        psutil.cpu_percent()
        self.disk_used_before = Monitor.get_disk_usage().used
        self.disk_rw_before = psutil.disk_io_counters()
        self.network_io_before = psutil.net_io_counters()

        return

    @staticmethod
    def get_cpu_percent(interval=1.0):
        """Get the current CPU utilization percentage.

        The percentage of used memory is calculated as follows:
        percent = (total - available) / total * 100

        Parameters
        ----------
        interval : float
            When interval is > 0.0, the method gets the CPU utilization
            percentage by comparing the system CPU times before and after the
            interval (blocking).
            When interval is 0.0 or None, the method gets the CPU utilization
            percentage by comparing the system CPU times since last call
            (returning immediately). For the first call, it will return a
            meaningless 0.0. In this case, it is recommended for accuracy that
            this function be called with at least 0.1 seconds between calls.

        Returns
        -------
        float
            The current CPU utilization percentage.

        """

        # Return the current CPU utilization percentage.
        return psutil.cpu_percent(interval)

    @staticmethod
    def get_memory_usage():
        """Get the memory usage statistics in MB.

        Returns
        -------
        namedtuple('memory_usage', ['total', 'available', 'used', 'percent'])
            A namedtuple containing the memory usage statistics. The field
            `total` is the total amount of physical memory in MB. The field
            `available` is the current amount of available memory in MB. The
            field `percent` is the current percentage of used memory:
            (total - available) / total * 100.

        """

        # Get the details of the current memory usage.
        current_memory_usage = psutil.virtual_memory()

        # Define a namedtuple for the results.
        memory_usage = collections.namedtuple(
            'memory_usage', ['total', 'available', 'used', 'percent'])

        # Return total, available, used, and percentage of used memory in MB.
        return memory_usage(current_memory_usage.total / 1024.0 / 1024,
                            current_memory_usage.available / 1024.0 / 1024,
                            (current_memory_usage.total -
                             current_memory_usage.available) / 1024.0 / 1024,
                            current_memory_usage.percent)

    @staticmethod
    def get_disk_usage():
        """Get the overall disk usage statistics in GB.

        There might be more than one disk attached to the machine. This
        method returns the overall total, used, free disk space in all disks.

        Returns
        -------
        namedtuple('disk_usage', ['total', 'used', 'free', 'percent'])
            A namedtuple containing the overall disk usage statistics. The
            field `total` is the total amount of disk space in GB. The field
            `used` is the total amount of used disk space in GB. The field
            `free` is the total amount of free disk space. The field `percent`
            is the overall percentage of used disk space (used / total * 100).

        """

        # The total, used, and free disk space.
        total = 0.0
        used = 0.0
        free = 0.0

        # For all the attached disks, add the total, used, and free disk space.
        for partition in psutil.disk_partitions():
            # Get the details of the current disk usage.
            current_disk_usage = psutil.disk_usage(partition.mountpoint)
            total += current_disk_usage.total
            used += current_disk_usage.used
            free += current_disk_usage.free

        # Convert from bytes to GBs.
        total /= 1024.0 * 1024 * 1024
        used /= 1024.0 * 1024 * 1024
        free /= 1024.0 * 1024 * 1024

        # Define a namedtuple for the results.
        disk_usage = collections.namedtuple(
            'disk_usage', ['total', 'used', 'free', 'percent'])

        # Return the total, used, free, and percentage of used disk usage.
        return disk_usage(total, used, free, used / total * 100)

    @staticmethod
    def get_disk_rw(interval=1.0):
        """Get the overall disk read-write statistics.

        There might be more than one disk attached to the machine. This
        method returns the overall statistics for all disks.

        Parameters
        ----------
        interval : float
            The interval in which the method calculates the disk read-write
            statistics.

        Returns
        -------
        namedtuple('disk_rw', ['read_rate', 'write_rate'])
            A namedtuple containing the overall disk read-write statistics. The
            field `read_rate` is the reading rate in Mbps. The field
            `write_rate` is the write rate in Mbps.

        """

        # The timestamp before the first call.
        start_timestamp = time.time()

        # Get the current disk read-write numbers.
        disk_rw_before = psutil.disk_io_counters()

        # Sleep for the specified interval.
        time.sleep(interval)

        # The actual interval between the first and the second calls.
        actual_interval = time.time() - start_timestamp

        # Get the current disk read-write numbers.
        disk_rw_after = psutil.disk_io_counters()

        # The reading rate in Mbps.
        read_rate = disk_rw_after.read_bytes - disk_rw_before.read_bytes
        read_rate = read_rate * 8 / 1024.0 / 1024 / actual_interval

        # The writing rate in Mbps.
        write_rate = disk_rw_after.write_bytes - disk_rw_before.write_bytes
        write_rate = write_rate * 8 / 1024.0 / 1024 / actual_interval

        # Define a namedtuple for the results, and return it.
        disk_rw = collections.namedtuple('disk_rw', ['read_rate', 'write_rate'])
        return disk_rw(read_rate, write_rate)

    @staticmethod
    def get_network_io(interval=1.0):
        """Get the overall network input-output statistics.

        There might be more than network interface. This method returns the
        overall statistics for all network interfaces.

        Parameters
        ----------
        interval : float
            The interval in which the method calculates the network read-write
            statistics.

        Returns
        -------
        namedtuple('network_io', ['in_rate', 'out_rate'])
            A namedtuple containing the overall network input-output statistics.
            The field `in_rate` is the input rate in Mbps. The field
            `out_rate` is the output rate in Mbps.

        """

        # The timestamp before the first call.
        start_timestamp = time.time()

        # Get the current network input-output numbers.
        network_io_before = psutil.net_io_counters()

        # Sleep for the specified interval.
        time.sleep(interval)

        # The actual interval between the first and the second calls.
        actual_interval = time.time() - start_timestamp

        # Get the current network input-output numbers.
        network_io_after = psutil.net_io_counters()

        # The input rate in Mbps.
        in_rate = network_io_after.bytes_recv - network_io_before.bytes_recv
        in_rate = in_rate * 8 / 1024.0 / 1024 / actual_interval

        # The output rate in Mbps.
        out_rate = network_io_after.bytes_sent - network_io_before.bytes_sent
        out_rate = out_rate * 8 / 1024.0 / 1024 / actual_interval

        # Define a namedtuple for the results, and return it.
        network_io = collections.namedtuple('network_io',
                                            ['in_rate', 'out_rate'])
        return network_io(in_rate, out_rate)

    def get_all_stats(self):

        # The actual interval between the first and the second calls.
        actual_interval = time.time() - self.start_timestamp

        # Return the current CPU utilization percentage.
        cpu_percent = psutil.cpu_percent()
        # Get the current disk read-write numbers.
        disk_rw_after = psutil.disk_io_counters()
        # Get the current network input-output numbers.
        network_io_after = psutil.net_io_counters()

        # The disk reading and writing rate in Mbps.
        read_rate = disk_rw_after.read_bytes - self.disk_rw_before.read_bytes
        read_rate = read_rate * 8 / 1024.0 / 1024 / actual_interval
        write_rate = disk_rw_after.write_bytes - self.disk_rw_before.write_bytes
        write_rate = write_rate * 8 / 1024.0 / 1024 / actual_interval

        # The network input and output rate in Mbps.
        in_rate = network_io_after.bytes_recv - \
                  self.network_io_before.bytes_recv
        in_rate = in_rate * 8 / 1024.0 / 1024 / actual_interval
        out_rate = network_io_after.bytes_sent - \
                   self.network_io_before.bytes_sent
        out_rate = out_rate * 8 / 1024.0 / 1024 / actual_interval

        # Define a namedtuple for the results, and return it.
        stats = collections.namedtuple(
            'stats', ['cpu_percent', 'disk_consumption', 'read_rate',
                      'write_rate', 'in_rate', 'out_rate'])
        return stats(cpu_percent, Monitor.get_disk_usage().used -
                     self.disk_used_before, read_rate, write_rate, in_rate,
                     out_rate)


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == 'single':
        print
        print 'CPU Utilization Percentage: {}%'.format(Monitor.get_cpu_percent(1))

        memory_usage = Monitor.get_memory_usage()
        print
        print 'Memory'
        print 'Total Memory: {} MB'.format(memory_usage.total)
        print 'Available Memory: {} MB'.format(memory_usage.available)
        print 'Used Memory Percentage: {}%'.format(memory_usage.percent)

        disk_usage = Monitor.get_disk_usage()
        print
        print 'Disk'
        print 'Total Disk: {} GB'.format(disk_usage.total)
        print 'Used Disk: {} GB'.format(disk_usage.used)
        print 'Free Disk: {} GB'.format(disk_usage.free)
        print 'Used Disk Percentage: {}%'.format(disk_usage.percent)

        disk_rw = Monitor.get_disk_rw(1)
        print
        print 'Disk IO'
        print 'Reading Rate: {} Mbps'.format(disk_rw.read_rate)
        print 'Writing Rate: {} Mbps'.format(disk_rw.write_rate)

        network_io = Monitor.get_network_io(1)
        print
        print 'Network IO'
        print 'Input Rate: {} Mbps'.format(network_io.in_rate)
        print 'output Rate: {} Mbps'.format(network_io.out_rate)
        exit(1)

    with open("log.txt", "w", 1) as f:

        h = '\t'.join(['CPU', 'Mem', 'Dsk', 'Dsk R', 'Dsk W', 'Net I', 'Net O'])
        h2 = '\t'.join(['%', '%', '%', 'Mbps', 'Mbps', 'Mbps', 'Mbps'])

        print h
        print h2
        f.write(h + '\n')
        f.write(h2 + '\n')

        while True:

            # The timestamp at the beginning of the iteration.
            start_timestamp = time.time()

            output = []
            output.append(Monitor.get_cpu_percent(3))
            output.append(Monitor.get_memory_usage().percent)
            output.append(Monitor.get_disk_usage().percent)

            disk_rw = Monitor.get_disk_rw(3)
            output.append(disk_rw.read_rate)
            output.append(disk_rw.write_rate)

            network_io = Monitor.get_network_io(3)
            output.append(network_io.in_rate)
            output.append(network_io.out_rate)

            output = ['%.3f' % elem for elem in output]

            output.append(str(datetime.datetime.now()))
            output = '\t'.join(map(str, output))

            print output
            f.write(output + '\n')

            # Sleep so that the total time of the iteration is 10 seconds.
            time.sleep(10 - (time.time() - start_timestamp))